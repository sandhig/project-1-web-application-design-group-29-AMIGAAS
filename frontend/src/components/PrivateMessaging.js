import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';

function PrivateMessage({ currentUserId }) {
    const { userId } = useParams();
    const [conversationId, setConversationId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const ws = useRef(null);
    const isUnmounting = useRef(false);

    useEffect(() => {
        console.log("fetch convo")
        // Start or get the conversation
        fetch(`http://localhost:8000/api/conversation/start/${userId}/`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            setConversationId(data.conversation_id);
        });
    }, [userId]);

    useEffect(() => {
        if (conversationId) {
            console.log(conversationId)
            // Fetch messages
            fetch(`http://localhost:8000/api/conversation/${conversationId}/messages/`)
                .then(response => response.json())
                .then(data => {
                    setMessages(data.messages);
                });

            ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${conversationId}/`);

            ws.current.onmessage = function (e) {
                const data = JSON.parse(e.data);
                const message = data.message;

                setMessages(prevMessages => {
                    if (prevMessages.some(m => m.id === message.id)) {
                        return prevMessages;
                    }
                    return [...prevMessages, message];
                });
            };

            ws.current.onclose = function (e) {
                if (!isUnmounting.current) {
                    console.error('Chat socket closed unexpectedly');
                } else {
                    console.log('Chat socket closed due to component unmounting');
                }
            };

            return () => {
                isUnmounting.current = true;
                if (ws.current) {
                    ws.current.close();
                }
            };
        }
    }, [conversationId]);

    const sendMessage = () => {
        if (input.trim() !== '') {
            ws.current.send(
                JSON.stringify({
                    content: input,
                    sender_id: currentUserId,
                })
            );
            setInput('');
        }
    };

    if (!conversationId) {
        return <div>Loading conversation...</div>;
    }

    return (
        <div>
            <div>
                {messages.map(message => (
                    <div key={message.id}>
                        <strong>{message.sender_name}:</strong> {message.content}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyPress={e => {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                }}
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default PrivateMessage;
