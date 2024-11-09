// FAQ.js
import React, { useState } from 'react';
import Header from "../../components/Header"

function FAQ() {
  const faqData = [
    { question: 'How do I buy items on this platform?', answer: 'Simply browse listings and contact the seller for further details.' },
    { question: 'Can we meet sellers outside of UofT locations?', answer: 'For safety, we do not reccommend it, but that can be discussed with the seller of the item(s).' },
    // Add more FAQs as needed
  ];

  return (
    <div className="faq-section">
        <Header/>
         <div style={{ padding: '20px' }}></div>
      <h2>Frequently Asked Questions</h2>
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
      <div className="faq-question" onClick={toggleOpen}>
        <h3>{question}</h3>
        <span>{isOpen ? '-' : '+'}</span>
      </div>
      {isOpen && <p className="faq-answer">{answer}</p>}
    </div>
  );
}

export default FAQ;
