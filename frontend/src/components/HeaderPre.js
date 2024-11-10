import { useNavigate } from 'react-router-dom';
import './Header.css'

function HeaderPre() {
  const navigate = useNavigate();

  const handleWelcome = () => {
    navigate('/'); //Redirects to the index (home) page
  }

  return (
    <div className="header">
      <div className="logo-container"
        id="logo" 
        onClick={handleWelcome} 
        style={{
            cursor: 'pointer', // Changes cursor to indicate it's clickable
        }}
      >
          <img className="header-logo" src="/images/header-logo-navy-cyan-white.png" alt="Website logo"></img>
          <div className="site-title">TOO GOOD TO THROW</div>
      </div>
    </div>
  );
};

export default HeaderPre;

