document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    menuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
    });

    // Change navbar background on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});



/*Used for section */
const infoSection = document.getElementById("infoSection");

function showInfo(industry) {
    // Remove the 'selected' class from all boxes
    const boxes = document.querySelectorAll('.right-section .box');
    boxes.forEach(box => box.classList.remove('selected'));

    // Add the 'selected' class to the clicked box
    event.target.classList.add('selected');

    // Update the left section content based on the selected industry
    let title = '';
    let content = '';
    switch(industry) {
        case 'Education':
            title = 'Education Solutions';
            content = 'EMO-TRACK helps students and teachers stay connected in virtual classrooms, creating better educational experiences for everyone.';
            break;
        case 'Financial Services':
            title = 'Financial Services Solutions';
            content = 'EMO-TRACK enables secure communications for financial institutions, improving collaboration and customer relationships.';
            break;
        case 'Government':
            title = 'Government Solutions';
            content = 'EMO-TRACK provides governments with the tools to streamline services, securely collaborate, and engage with citizens more effectively.';
            break;
        case 'Healthcare':
            title = 'Healthcare Solutions';
            content = 'EMO-TRACK enhances healthcare delivery through telemedicine, allowing patients and providers to connect anytime, anywhere.';
            break;
        case 'Manufacturing':
            title = 'Manufacturing Solutions';
            content = 'EMO-TRACK helps manufacturers improve operations, collaborate across teams, and streamline processes for greater efficiency.';
            break;
        case 'Retail':
            title = 'Retail Solutions';
            content = 'EMO-TRACK assists retailers in connecting with customers, improving operations, and delivering better service across multiple channels.';
            break;
    }

    infoSection.innerHTML = `
        <h1>${title}</h1>
        <p>${content}</p>
        <button class="explore-btn">Explore Industry Solutions</button>
    `;
}



/*Information*/
  // JavaScript for carousel functionality
  const cardWrapper = document.querySelector('.card-wrapper');
  const cards = document.querySelectorAll('.card');
  const prevButton = document.getElementById('prev');
  const nextButton = document.getElementById('next');
  const cardWidth = cards[0].offsetWidth;
  const visibleCards = 3;
  const totalCards = cards.length;
  let currentIndex = 0;

  function updateCarousel() {
    const maxIndex = totalCards - visibleCards;
    const offset = Math.min(currentIndex, maxIndex) * cardWidth;
    cardWrapper.style.transform = `translateX(-${offset}px)`;
  }

  nextButton.addEventListener('click', () => {
    if (currentIndex < totalCards - visibleCards) {
      currentIndex++;
      updateCarousel();
    }
  });

  prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
      updateCarousel();
    }
  });

  // Initialize carousel
  updateCarousel();