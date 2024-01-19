<div align="center">
  <img src="" alt="Home Page">
</div>


## Table of Contents

1.  <details open>
        <summary><a href="#ux">UX</a></summary>

      <ul>
      <li><details>
      <summary><a href="#goals">Goals</a></summary>

      - [Visitor Goals](#visitor-goals)
      - [User Stories](#user-stories)
      </details></li>

      <li><details>
      <summary><a href="#visual-design">Visual Design</a></summary>

      - [Wireframes](#wireframes)
      - [Fonts](#fonts)
      - [Icons](#icons)
      - [Colors](#colors)
      </details></li>
      </ul>

    </details>

2.  <details open>
        <summary><a href="#features">Features</a></summary>

      <ul>
      <li><details>
      <summary><a href="#page-elements">Page Elements</a></summary>

      - [All Pages](#all-pages)
      - [Index Page](#index-page)
      - [About Page](#about-page)
      - [Contact Page](#contact-page)
      </details></li>

      <li><details>
      <summary><a href="#feature-ideas">Feature Ideas</a></summary>

      - [Basic](#basic)
      - [Content](#content)
      </details></li>
      </ul>

    </details>

3.  <details open>
        <summary><a href="#technologies-used">Technologies Used</a></summary>

      - [Languages](#languages)
      - [Frameworks](#frameworks)
      - [Libraries](#libraries)
      - [APIs](#apis)
      - [Platforms](#platforms)
      - [Other Tools](#other-tools)

    </details>

4.  <details open>
        <summary><a href="#testing">Testing</a></summary>

      <ul>
      <li><details>
      <summary><a href="#methods">Methods</a></summary>

      - [Validation](#validation)
      - [Manual Testing](#manual-testing)
      </details></li>

      <li><details>
      <summary><a href="#bugs">Bugs</a></summary>

      - [Known Bugs](#known-bugs)
      - [Fixed Bugs](#fixed-bugs)
      </details></li>
      </ul>

    </details>

5. <a href="#deployment">Deployment</a>

6.  <details open>
        <summary><a href="#credits">Credits</a></summary>

      - [Images](#images)
      - [Writing](#writing)
      
    </details>

7. <a href="#contributors">Contributors</a>

---

# UX

## Goals

### Visitor Goals

User goals are:

- 

### User Stories

1. 

## Visual Design

### Wireframes

Wireframes: To see the wireframes created at the UX stage [Click Here!]()

### Fonts

<div align="center">
  <img src="" alt="Font">
</div>
<div align="center">
  <img src="" alt="Font">
</div>

- The primary font, [xxxxx]() was chosen because.....
- The secondary font, [xxxxxx]() was chosen because....

### Icons

<div align="center">
  <img src="./Readme_Images/HolyFavicons.png" alt="Icons">
</div>

- Icons are taken from the [Fontawesome](https://fontawesome.com/) Icon library and are utilised as classes in the `<i>` tag.
- As they are utilised as classes, they can easily be styled using other classes or IDs in the same tag. I often used Bootstrap classes to style them uniformly.
- Icons are utilised as decoration for the page, adding flair to buttons that convey meaning as to their purpose secondary to the text description, an icon is often recognised quicker than what we read so this give a more fluid user experience when navigating the site

---

# Features

## Page Elements

### All Pages

#### Navbar

<div align="center">
  <img src="" alt="Medium Header">
  <img src="" alt="Small Header">
</div>

- The Navbar is simple, providing only four options, the home page so the user can always access the landing page if they wish, an about page detailing the origin and expertise of HolyRecipes, a contact page if the user has any needs they want to convery to HolyRecipes and a search box so the user can look for all the recipes on the sites using any parameter they wish
- The Logo is always highlighted, swapping size as necessary depending on device size.
- On smaller devices, the menu becomes collapsible.
- The mobile nav button has been placed to the right for ease of use with one hand.
- The navbar is fixed so it is visible no matter how far you scroll.

#### Footer

<div align="center">
  <img src="" alt="Footer">
</div>

#### Feature

-

### Index Page

#### Carousel

<div align="center">
  <img src="" alt="Carousel Gif">
</div>



### About Page

<div align="center">
  <img src="" alt="About">
</div>

-

### Contact Page

<div align="center">
  <img src="" alt="Contact Page">
</div>

- A friendly and welcoming page that invites questions and uses [EmailJS](https://www.emailjs.com/) to send the emails.
- The form has validation and is fully responsive.
- Once the send button is pressed, a message will appear letting the user know if the message is successful or has failed

## Feature Ideas

### Basic

- 

### Content

- 

---

# Technologies Used

## Languages

- [HTML](w3.org/standards/webdesign/htmlcss)
  - Page markup.
- [CSS](w3.org/standards/webdesign/htmlcss)
  - Styling.
- [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
  - Running functions for interactive components, AJAX, etc.

## Frameworks

- [Bootstrap 5](https://getbootstrap.com/)
  - Used for basic styles and outline.

## Libraries

- [JQuery](https://jquery.com/)
  - Animations and click functions.
- [Google Fonts](https://fonts.google.com)
  - Font Styles.
- [Fontawesome](https://fontawesome.com/)
  - Used for icons

## APIs

- [EmailJS](https://www.emailjs.com/)
   - EmailAPI used for having a contact page with no backend

## Platforms

- [Github](https://github.com/)
  - Storing code remotely and deployment.  
- [Gitpod](https://gitpod.io/)
  - IDE for project development.

## Other Tools

- [Balsamiq](https://balsamiq.com/)
  - To create wireframes.
- [Favicon Generator](https://www.favicon-generator.org/)
  - Favicons
- [Coolors](https://coolors.co/)
  - Creating color pallettes.

---

# Testing

## Methods

### Validation

- HTML has been validated with [W3C HTML5 Validator](https://validator.w3.org/).
- CSS has been validated with [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
- Links checked with [W3C Link Checker](https://validator.w3.org/checklink).

- Google Lighthouse tool was used to assess the web-site

### Manual Testing
**TEST** | **ACTION** | **EXPECTATION** | **RESULT** 
----------|----------|----------|----------
Index | Size to 320px by 800px using Chrome Dev Tools	| Elements look good @ 320px by 800px | Works as expected
Index | Size to 1920px by 1080px using Chrome Dev Tools | Elements look good 1920px by 1080px | Works as expected
About | Size to 320px by 800px using Chrome Dev Tools	| Elements look good @ 320px by 800px | Works as expected
About | Size to 1920px by 1080px using Chrome Dev Tools | Elements look good 1920px by 1080px | Works as expected
Contact | Size to 320px by 800px using Chrome Dev Tools	| Elements look good @ 320px by 800px | Works as expected
Contact | Size to 1920px by 1080px using Chrome Dev Tools | Elements look good 1920px by 1080px | Works as expected
Index page test | All phone sizes checked using Chrome Dev Tools | Elements look good | Works at expected
About page test | All phone sizes checked using Chrome Dev Tools | Elements look good | Works at expected
Contact page test | All phone sizes checked using Chrome Dev Tools | Elements look good | Works at expected

## Bugs

### Fixed Bugs

- 

---

## Deployment

- The site was deployed to GitHub pages. The steps to deploy are as follows:
  - In the GitHub repository, navigate to the Settings tab
  - From the source section drop-down menu, select the Master Branch
  - Once the master branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

The live link can be found [HERE]()

## Credits

#### Images

- 

#### Writing

- 

## Contributors

- [Liam](https://github.com/caleom)

---
