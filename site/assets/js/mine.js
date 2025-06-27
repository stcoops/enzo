document.getElementById("wip-banner")
        .addEventListener("click", function() {

  document.getElementById("wip-banner").id = "wip-banner-fade-out";
});

document.getElementById("wip-banner-mobile")
        .addEventListener("click", function() {

  document.getElementById("wip-banner-mobile").id = "wip-banner-fade-out-mobile";
});




const events = document.querySelectorAll('.timeline-event');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    } else {
      entry.target.classList.remove('visible');
    }
  });
}, {
  threshold: 0.9
});

events.forEach(event => {
  observer.observe(event);
});



// Handle initial page load
        window.addEventListener('load', () => {
            const hash = window.location.hash.substr(1);
            showPage(hash || 'welcome');
        });

        // Handle navigation clicks
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageId = e.target.getAttribute('href').substr(1);
                showPage(pageId);
                history.pushState(null, null, `#${pageId}`);
            });
        });

        // Handle browser back/forward
        window.addEventListener('popstate', () => {
            const hash = window.location.hash.substr(1);
            showPage(hash || 'welcome');
        });

        function showPage(pageId) {
            document.querySelectorAll('.page').forEach(page => {
                page.classList.remove('active');
            });
            document.getElementById(pageId).classList.add('active');
        }

/*
document.getElementById("submit").addEventListener("click", function() {
  fields.name = document.getElementById('name');
  fields.email = document.getElementById('email');
  fields.message = document.getElementById('message');
})

class User {
  constructor(firstName, lastName, gender, address, country, email, newsletter, question) {
  this.firstName = firstName;
  this.lastName = lastName;
  this.gender = gender;
  this.address = address;
  this.country = country;
  this.email = email;
  this.newsletter = newsletter;
  this.question = question;
  }
 }




function isNotEmpty(value) {
  if (value == null || typeof value == 'undefined' ) return false;
  return (value.length > 0);
}

function isEmail(email) {
  let regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  return regex.test(String(email).toLowerCase());
}

function isValid() {
  var valid = true;
  
  valid &= fieldValidation(fields.name, isNotEmpty);
  valid &= fieldValidation(fields.email, isEmail);
  valid &= fieldValidation(fields.message, isNotEmpty);
 
  return valid;
 }

*/