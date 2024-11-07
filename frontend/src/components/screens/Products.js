import React, { useState, useEffect, useRef } from "react";
import './Products.css';
import { useUser } from '../../context/UserContext';
import { useNavigate } from 'react-router-dom';
import IconButton from "@mui/material/IconButton";
import PauseIcon from '@mui/icons-material/Pause';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import ArrowLeftIcon from '@mui/icons-material/ArrowLeft';
import Header from "../../components/Header"
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [isPlaying, setIsPlaying] = useState(true);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('authToken');
  const { currentUser } = useUser();
  const navigate = useNavigate();

  const hour = parseInt(new Date().getHours());
  let greeting = '';
  if (5 <= hour && hour <= 11) {
    greeting = 'Good morning';
  } else if (12 <= hour && hour <= 17) {
    greeting = 'Good afternoon';
  } else if (18 <= hour && hour <= 20) {
    greeting = 'Good evening';
  } else if ((21 <= hour && hour <= 23) || hour <= 4) {
    greeting = 'Welcome back';
  }

  const responsive = {
    allScreens: {
      breakpoint: { max: 4000, min: 0 },
      items: 1,
    },
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  useEffect(() => {
    fetch('http://3.87.240.14:8000/api/products/', {
      headers: {
        'Authorization': `Token ${token}`,
      }
    })
      .then(response => response.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch(error => console.error('Error fetching products:', error));
  }, []);

  const handleOpenProduct = (id) => {
    navigate(`/products/${id}`);
  };

  const scrollContainerRef = useRef(null);

  const scrollLeft = () => {
    const itemWidth = scrollContainerRef.current.children[0].offsetWidth;
    scrollContainerRef.current.scrollBy({ left: -itemWidth, behavior: "smooth" });
  };

  const scrollRight = () => {
    const itemWidth = scrollContainerRef.current.children[0].offsetWidth;
    scrollContainerRef.current.scrollBy({ left: itemWidth, behavior: "smooth" });
  };

  return (
    <div>
      <Header />
      <div className="product-grid">
          {currentUser ? (<h1 style={{textAlign: "left", padding: "0 45px", margin: "35px 0 0 0"}}>{greeting}, {currentUser.first_name}</h1>) : null} 
          
          <div className="carousel-container">
            <Carousel
              responsive={responsive}
              swipeable={true}
              draggable={true}
              showDots={true}
              infinite={true}
              autoPlay={isPlaying} 
              autoPlaySpeed={4000}
              keyBoardControl={true}
              customTransition="all 0.5s"
              transitionDuration={500}
              containerClass="carousel-container"
              removeArrowOnDeviceType={["tablet", "mobile"]}
              dotListClass="line-dot-style"
              itemClass="carousel-item-padding-40-px"
            >
              <img src="/images/carousel/1.png"></img>
              <img src="/images/carousel/2.png"></img>
              <img src="/images/carousel/3.png"></img>
            </Carousel>
            <IconButton onClick={handlePlayPause} className="play-pause-button">
              {isPlaying ? (<PauseIcon style={{ fill: "white" }} />) : (<PlayArrowIcon style={{ fill: "white" }} />)}
            </IconButton>
          </div>
        
          <div className="title">Page Turners</div>

          <div style={{ display: "flex", alignItems: "center" }}>

            <IconButton onClick={scrollLeft}>
              <ArrowLeftIcon style={{ fontSize: "xxx-large" }} />
            </IconButton>

            <div className="scroll-container" ref={scrollContainerRef}>
              {loading ? (
                <span className="product-loader"></span>
              ) : (
                <>
                {products
                  .filter(product => product.category === "Textbook")
                  .map(product => (
                  <div key={product.id} className="product-item">
                    <div onClick={() => handleOpenProduct(product.id)}>
                  
                      {product.image_url ? 
                      (<img className="product-image" src={product.image_url}></img>) 
                      : <img className="product-image" src="/images/no-image-icon.png"></img>}
                      
                      <div className="product-text">
                        <div className="product-price">${product.price}</div>
                        <div className="product-title">{product.name}</div>
                        <div className="product-location">{product.pickup_location}</div>
                      </div>
                    </div>
                  </div>
                ))}
                </>
              )}
            </div>

            <IconButton onClick={scrollRight}>
              <ArrowRightIcon style={{ fontSize: "xxx-large" }} />
            </IconButton>

          </div>

          <div className="title">Fashion Finds</div>

          <div style={{ display: "flex", alignItems: "center" }}>

            <IconButton onClick={scrollLeft}>
              <ArrowLeftIcon style={{ fontSize: "xxx-large" }} />
            </IconButton>

            <div className="scroll-container" ref={scrollContainerRef}>
            {loading ? (
                <span className="product-loader"></span>
              ) : (
                <>
                {products
                  .filter(product => product.category === "Clothing")
                  .map(product => (
                  <div key={product.id} className="product-item">
                    <div onClick={() => handleOpenProduct(product.id)}>
                      {product.image_url ? 
                      (<img className="product-image" src={product.image_url}></img>) 
                      : <img className="product-image" src="/images/no-image-icon.png"></img>}
                      
                      <div className="product-text">
                        <div className="product-price">${product.price}</div>
                        <div className="product-title">{product.name}</div>
                        <div className="product-location">{product.pickup_location}</div>
                      </div>
                    </div>
                  </div>
                ))}
                </>
              )}
            </div>

            <IconButton onClick={scrollRight}>
              <ArrowRightIcon style={{ fontSize: "xxx-large" }} />
            </IconButton>

          </div>

          <div className="title">Dorm Essentials</div>

          <div style={{ display: "flex", alignItems: "center" }}>

            <IconButton onClick={scrollLeft}>
              <ArrowLeftIcon style={{ fontSize: "xxx-large" }} />
            </IconButton>

            <div className="scroll-container" ref={scrollContainerRef}>
            {loading ? (
                <span className="product-loader"></span>
              ) : (
                <>
                {products
                  .filter(product => product.category === "Furniture")
                  .map(product => (
                  <div key={product.id} className="product-item">
                    <div onClick={() => handleOpenProduct(product.id)}>
                      {product.image_url ? 
                      (<img className="product-image" src={product.image_url}></img>) 
                      : <img className="product-image" src="/images/no-image-icon.png"></img>}
                      
                      <div className="product-text">
                        <div className="product-price">${product.price}</div>
                        <div className="product-title">{product.name}</div>
                        <div className="product-location">{product.pickup_location}</div>
                      </div>
                    </div>
                  </div>
                ))}
                </>
              )}
            </div>

            <IconButton onClick={scrollRight}>
              <ArrowRightIcon style={{ fontSize: "xxx-large" }} />
            </IconButton>

          </div>

        </div>
    </div>
  );
};

export default Products;