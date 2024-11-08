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
import { Link } from 'react-router-dom';


const Products = () => {
  const [products, setProducts] = useState([]);
  const [isPlaying, setIsPlaying] = useState(true);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('authToken');
  const { currentUser } = useUser();
  const navigate = useNavigate();

  const scrollContainerRefs = useRef([]);

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

  const scrollLeft = (index) => {
    const itemWidth = scrollContainerRefs.current[index].children[0].offsetWidth;
    scrollContainerRefs.current[index].scrollBy({ left: -itemWidth, behavior: "smooth" });
  };

  const scrollRight = (index) => {
    const itemWidth = scrollContainerRefs.current[index].children[0].offsetWidth;
    scrollContainerRefs.current[index].scrollBy({ left: itemWidth, behavior: "smooth" });
  };

  const categories = [
    { name: "Textbook", title: "Page Turners" },
    { name: "Clothing", title: "Fashion Finds" },
    { name: "Furniture", title: "Dorm Essentials" }
  ];

  return (
    <div>
      <Header />
      <div className="product-grid">
          
          {currentUser ? (
              <div className="header-container">
                  <h1 style={{ textAlign: "left", padding: "0 45px", margin: "35px 0 0 0" }}>
                      {greeting}, {currentUser.first_name}
                  </h1>
                  <div className="help-settings-container">
                      <Link to="/help-settings" className="help-settings-button">
                          Help & Settings
                      </Link>
                  </div>
              </div>) : null}

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

          {categories.map((category, index) => (
            <div key={index}>
              <div className="title">{category.title}</div>

              <div style={{ display: "flex", alignItems: "center" }}>

                <IconButton onClick={() => scrollLeft(index)}>
                  <ArrowLeftIcon style={{ fontSize: "xxx-large" }} />
                </IconButton>

                <div className="scroll-container" ref={(el) => (scrollContainerRefs.current[index] = el)}>
                  {loading ? (
                    <span className="product-loader"></span>
                  ) : (
                    <>
                    {products
                      .filter(product => product.category === category.name)
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

                <IconButton onClick={() => scrollRight(index)}>
                  <ArrowRightIcon style={{ fontSize: "xxx-large" }} />
                </IconButton>

              </div>
            </div>
          ))}

        </div>
    </div>
  );
};

export default Products;