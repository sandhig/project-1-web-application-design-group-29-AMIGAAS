/* FAQ.js */

import React, { useState } from 'react';
import Header from "../../components/Header"
import './FAQ.css';


function FAQ() {
  const faqData = [
    { question: 'How do I buy items on this platform?', answer: 'Simply browse listings and contact the seller for further details.' },
    { question: 'Can we meet sellers outside of UofT locations?', answer: 'For safety, we do not recommend it, but that can be discussed with the seller of the item(s).' },
    { question: 'How do I sell an item?', answer: 'Go to "New Listing" in the menu, fill in the required details about the item, and submit. Your listing will then be available for other students to view and purchase.' },
    { question: 'Is there a fee for listing an item?', answer: 'No, listing items on Too Good to Throw is completely free.' },
    { question: 'How can I contact the buyer or seller?', answer: 'Once you’re interested in an item, you can use the private messaging feature to contact the buyer or seller directly through the platform.' },
    { question: 'What items are allowed for sale on this platform?', answer: 'Only second-hand items related to university life, such as textbooks, electronics, furniture, and clothing, are allowed.' },
    { question: 'What if I am not satisfied with the item I bought?', answer: 'Too Good to Throw does not handle returns or refunds. We recommend meeting the seller, examining the item carefully, and confirming all details before completing the purchase.' },
    { question: 'How are items organized on the platform?', answer: 'Items are organized by category, such as textbooks, furniture, electronics, and clothing, making it easier for you to find what you’re looking for.' },
    { question: 'What happens to my account after I graduate?', answer: 'A UofT email is required to login, so when you graduate you can still use your account so long as your email is still active. Once your email is deactivated you will not be able to use Too Good to Throw.' },
    { question: 'Are prices listed final?', answer: 'You can negotiate with the seller.' },
    // Add more FAQs as needed
  ];

  return (
    <div className="faq-section">
        <Header/>
         <div style={{ padding: '10px' }}></div>
      <h1 className="faq-title">Frequently Asked Questions</h1>
      {faqData.map((faq, index) => (
        <FAQItem key={index} question={faq.question} answer={faq.answer} />
      ))}
    </div>
  );
}

function FAQItem({ question, answer }) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleOpen = () => setIsOpen(!isOpen);

  return (
    <div className="faq-item">
      <div 
        className="faq-question" 
        onClick={toggleOpen} 
      >
        <h3 style={{ marginRight: '10px' }}>{question}</h3>
        <span>{isOpen ? '-' : '+'}</span>
      </div>
      {isOpen && <p className="faq-answer">{answer}</p>}
    </div>
  );
}

export default FAQ;


