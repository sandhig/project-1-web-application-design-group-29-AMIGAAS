import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import './PrivateMessage.css';
import { IoSend } from "react-icons/io5";
import { useUser } from '../context/UserContext';

function PrivateMessage() {
    const [conversations, setConversations] = useState([]);
    const [selectedConversationId, setSelectedConversationId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [hasConversations, setHasConversations] = useState(null);
    const ws = useRef(null);
    const location = useLocation();
    const selectedConversationRef = useRef(selectedConversationId);
    const loadingRef = useRef(loading);
    const messageBuffer = useRef([]);
    const isUnmounting = useRef(false);

    const { currentUser } = useUser();

    const token = localStorage.getItem('authToken');

    const fetchConversations = () => {
        if (currentUser) {
            fetch(`http://3.87.240.14:8000/api/conversations/`, {
                headers: {
                    'Authorization': `Token ${currentUser.token}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    setConversations(data.conversations);
                });
        }
    };

    // Connect to Websocket on initialization
    useEffect(() => {

        if (currentUser) {

            fetch(`http://3.87.240.14:8000/api/conversations/`, {
                headers: {
                    'Authorization': `Token ${currentUser.token}`,
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch conversations');
                }
                return response.json();
            })
            .then(data => {
                if (data['conversations'].length > 0) {
                    ws.current = new WebSocket(`ws://3.87.240.14:8000/ws/chat/user/${currentUser.id}/`);
                    
                    ws.current.onopen = function () {
                        console.log("WebSocket connection opened");
                        setHasConversations(true);
                        setConversations(data.conversations);
                    };

                    ws.current.onmessage = function (e) {
                        const data = JSON.parse(e.data);
                        const message = data.message;

                        if (selectedConversationRef.current && message.conversation_id === selectedConversationRef.current) {
                            if (loadingRef.current) {
                                messageBuffer.current.push(message);
                            } else {
                                setMessages(prevMessages => [...prevMessages, message]);
                                if (message.sender_id !== currentUser.id) {
                                    markMessagesAsRead([message.id])
                                }
                            }
                        }

                        fetchConversations();
                    };

                    ws.current.onclose = function () {
                        console.log("WebSocket connection closed");
                    };

                    ws.current.onerror = (error) => {
                        console.error("WebSocket error:", error);
                    };

                    return () => {
                        isUnmounting.current = true;
                        if (ws.current) {
                            ws.current.close();
                        }
                    };
                } else {
                    setHasConversations(false);
                }
            })
            .catch(error => {
                console.error("Error fetching conversations:", error);
                setHasConversations(false);
            });
        }

    }, [currentUser])

    useEffect(() => {

        fetchConversations();

        // Check if a user is selected
        const searchParams = new URLSearchParams(location.search);
        const userId = searchParams.get('userId');

        // Fetch or create conversation with user
        if (userId) {
            fetch(`http://3.87.240.14:8000/api/conversation/start/${userId}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {

                    setConversations(prevConversations => {
                        const existingConversation = prevConversations.find(convo => convo.id === data.conversation_id);
                        if (!existingConversation) {
                            return [...prevConversations, {
                                id: data.conversation_id,
                                name: data.name,
                                last_message: '',
                                last_sender_name: '',
                                last_sender_id: '',
                                is_read: true
                            }];
                        }
                        return prevConversations;
                    });

                    setSelectedConversationId(data.conversation_id);
                    setHasConversations(true);
                });
        }
    }, [location.search]);

    useEffect(() => {
        if (selectedConversationId) {
            
            setLoading(true);
            loadingRef.current = true;

            selectedConversationRef.current = selectedConversationId;

            // Fetch messages for the selected conversation
            fetch(`http://3.87.240.14:8000/api/conversation/${selectedConversationId}/messages/`, {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    setMessages(data.messages);
                    setLoading(false);
                    loadingRef.current = false;

                    if (messageBuffer.current.length > 0) {
                        setMessages(prevMessages => {
                            const updatedMessages = [...prevMessages, ...messageBuffer.current];
                            messageBuffer.current = [];
                            return updatedMessages;
                        });
                    }

                    lastReadMessageId = getLastReadMessageId();

                    if (data.messages) {
                        // Mark messages as read
                        const unreadMessageIds = data.messages
                            .filter(msg => !msg.read && msg.sender_id !== currentUser.id)
                            .map(msg => msg.id);
                        if (unreadMessageIds.length > 0) {
                            markMessagesAsRead(unreadMessageIds);
                        }
                    }
                });
        }
    }, [selectedConversationId]);

    const markMessagesAsRead = (messageIds) => {
        fetch(`http://3.87.240.14:8000/api/conversation/${selectedConversationRef.current}/mark_as_read/`, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${currentUser.token}`,
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    setMessages(prevMessages => {
                        prevMessages.map(msg =>
                            messageIds.includes(msg.id) ? { ...msg, read: true } : msg
                        )
                        return [...prevMessages];
                    });

                    fetchConversations();
                } else {
                    console.error('Failed to mark messages as read:', data.error);
                }
            })
            .catch(error => {
                console.error('Error marking messages as read:', error);
            });
    }

    const sendMessage = () => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN & input != '') {
            ws.current.send(
                JSON.stringify({
                    content: input,
                    sender_id: currentUser.id,
                    conversation_id: selectedConversationId
                })
            );
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

    const getLastReadMessageId = () => {
        if (messages) {
            const lastReadMessage = messages
                .filter(msg => msg.sender_id === currentUser.id && msg.read)
                .slice(-1)[0];
            return lastReadMessage ? lastReadMessage.id : null;
            }
        else {
            return null;
        }
    };

    let lastReadMessageId = getLastReadMessageId();

    if (hasConversations === null) {
        return <div>Loading...</div>;
    }

    if (hasConversations === false) {
        return <div>No messages</div>;
    }

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
                            <p>{conversation.last_sender_id == currentUser.id ? 'You' : conversation.last_sender_name}: {conversation.last_message}</p>
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
                                            {(i === 0 || (new Date(message.timestamp).getTime() - new Date(messages[i - 1].timestamp).getTime()) / (1000 * 3600) > 2) && (
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
                                            <div className={message.sender_id === currentUser.id ? 'from' : 'to'}>
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
                                                    {/*
                                        <div className="read-receipt">
                                            {message.id === lastReadMessageId && (
                                                <p>Read</p>
                                            )}
                                        </div>
                                        */}
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
