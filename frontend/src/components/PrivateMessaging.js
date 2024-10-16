import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import './PrivateMessage.css';
import { IoSend } from "react-icons/io5";

function PrivateMessage({ currentUserId }) {
    const [conversations, setConversations] = useState([]);
    const [selectedConversationId, setSelectedConversationId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const ws = useRef(null);
    const isUnmounting = useRef(false);
    const location = useLocation();

    const fetchConversations = () => {
        fetch(`http://localhost:8000/api/conversations/`)
            .then(response => response.json())
            .then(data => {
                setConversations(data.conversations);
            });
    };

    // Connect to Websocket on initialization
    useEffect(() => {
        ws.current = new WebSocket(`ws://localhost:8000/ws/chat/`);
        console.log("connected")

        ws.current.onmessage = function (e) {
            const data = JSON.parse(e.data);
            const message = data.message;
            console.log(message)
            console.log("got a message from conversation ", message.conversation_id)

            setMessages(prevMessages => {
                const conversationId = message.conversation_id;
                const updatedMessages = prevMessages[conversationId] || [];

                console.log('convo id:', conversationId)
                console.log('prevMessages:', prevMessages)
                console.log('updatedMessages', updatedMessages)

                if (updatedMessages?.some(m => m.id === message.id)) {
                    return prevMessages[conversationId];
                }

                return [...updatedMessages, message];
            });
            console.log("set messages")

            fetchConversations();

            console.log(conversations)
        };

        ws.current.onclose = function () {
            console.log("WebSocket connection closed");
        };

        return () => {
            isUnmounting.current = true;
            if (ws.current) {
                ws.current.close();
            }
        };

    }, [])

    useEffect(() => {
        
        fetchConversations();

        // Check if a user is selected
        const searchParams = new URLSearchParams(location.search);
        const userId = searchParams.get('userId');

        // Fetch or create conversation with user
        if (userId) {
            fetch(`http://localhost:8000/api/conversation/start/${userId}/`, {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                setSelectedConversationId(data.conversation_id);
                fetchConversations();
            });
        }
    }, [location.search]);

    useEffect(() => {
        if (selectedConversationId) {
            setLoading(true);

            // Fetch messages for the selected conversation
            fetch(`http://localhost:8000/api/conversation/${selectedConversationId}/messages/`)
                .then(response => response.json())
                .then(data => {
                    setMessages(prevMessages => ({
                        ...prevMessages[selectedConversationId],
                        [selectedConversationId]: data.messages
                    }));
                    
                    setLoading(false);

                    console.log("Got messages from conversation: ", selectedConversationId)

                    console.log(messages)

                    lastReadMessageId = getLastReadMessageId();

                    const unreadMessageIds = data.messages
                        .filter(msg => !msg.read && msg.sender_id !== currentUserId)
                        .map(msg => msg.id);

                    console.log("Unread message ids: ", unreadMessageIds)

                    if (unreadMessageIds.length > 0) {
                        console.log(unreadMessageIds)
                        fetch(`http://localhost:8000/api/conversation/${selectedConversationId}/mark_as_read/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                console.log('success')
                                setMessages(prevMessages =>
                                    prevMessages[selectedConversationId].map(msg =>
                                        unreadMessageIds.includes(msg.id) ? { ...msg, read: true } : msg
                                    )
                                );
                                console.log('set messages')
                                fetchConversations();
                                console.log('fetched')
                            } else {
                                console.error('Failed to mark messages as read:', data.error);
                            }
                        })
                        .catch(error => {
                            console.error('Error marking messages as read:', error);
                        });
                    }
                });

            console.log("?")
        }
    }, [selectedConversationId]);
    
    const sendMessage = () => {
        if (input !== '') {
            ws.current.send(
                JSON.stringify({
                    content: input,
                    sender_id: currentUserId,
                    conversation_id: selectedConversationId
                })
            );
            console.log("sent a message to ", selectedConversationId)
            setInput('');

            fetchConversations();
        }
    };

    const messageListRef = useRef(null);
    
    useEffect(() => {
        if (messageListRef.current) {
        messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
        }
    }, [messages]);

    const selectedConversation = conversations.find(c => c.id === selectedConversationId);

    console.log(messages)
    
    const getLastReadMessageId = () => {
        const lastReadMessage = messages
            .filter(msg => msg.sender_id === currentUserId && msg.read)
            .slice(-1)[0];
        return lastReadMessage ? lastReadMessage.id : null;
    };
    
    let lastReadMessageId = 0;

    return (
        <div className="container">
            <div className="conversations">
                <h2>Chats</h2>
                {conversations.map(conversation => (
                    <div key={conversation.id} onClick={() => setSelectedConversationId(conversation.id)}
                        className={conversation.id === selectedConversationId ? 'selected' : '' || !conversation.is_read ? 'unread' : ''}>
                        <span className={!conversation.is_read ? 'dot' : ''}></span> 
                        <span className="title">
                            {conversation.name}
                            <p>{conversation.last_sender_id == currentUserId ? 'You': conversation.last_sender_name}: {conversation.last_message}</p>
                        </span>
                    </div>
                ))}
            </div>
            <div className="messages">
                {selectedConversationId ? (
                    <div className='messages-container'>
                        <h2>
                            {selectedConversation ? selectedConversation.name : ''}
                        </h2>
                        {loading ? (
                            <div>Loading...</div>
                        ) : (
                        <div className='messages-inner-container'>
                            <div className="message-list" ref={messageListRef}>
                                {messages.map((message, i) => (
                                    <div key={message.id}>
                                        {(i === 0 || (new Date(message.timestamp).getTime() - new Date(messages[i-1].timestamp).getTime())/(1000 * 3600) > 2) && (
                                            <div className="timestamp">
                                                {new Date(message.timestamp).toLocaleString('en-US', {
                                                    year: 'numeric',
                                                    month: 'short',
                                                    day: 'numeric',
                                                    hour: 'numeric',
                                                    minute: 'numeric',
                                                    hour12: true
                                                })}
                                            </div>
                                        )}
                                <div className={message.sender_id === currentUserId ? 'from' : 'to'}>
                                    <div className="message-container">
                                        <div className='message'>
                                            {message.content}
                                            <span className="time">{
                                                new Date(message.timestamp).toLocaleString('en-US', {
                                                    hour: 'numeric',
                                                    minute: 'numeric',
                                                    hour12: true
                                            })}</span>
                                        </div>
                                        <div className="read-receipt">
                                            {message.id === lastReadMessageId && (
                                                <p>Read</p>
                                            )}
                                        </div>
                                    </div>
                                </div>
                                </div>
                                ))}
                            </div>
                            
                            <div className="text-input">
                                <input type="text" value={input} onChange={e => setInput(e.target.value)}
                                    onKeyPress={e => {
                                        if (e.key === 'Enter') {
                                            sendMessage();
                                        }
                                    }}
                                />
                                <button onClick={sendMessage}><IoSend /></button>
                            </div>
                        </div>
                        )}
                    </div>
                ) : (
                    <div>Select a conversation</div>
                )}
            </div>
      </div>
    );
}

export default PrivateMessage;
