// Course data - will be loaded from courses.json
let courses = [];

// Load courses from JSON file
async function loadCoursesData() {
  try {
    const response = await fetch("courses.json");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    courses = data.courses;
    console.log("Courses loaded successfully:", courses.length, "courses");
    return courses;
  } catch (error) {
    console.error("Error loading courses:", error);
    // Fallback to hardcoded courses if JSON fails to load
    courses = getFallbackCourses();
    console.log("Using fallback courses:", courses.length, "courses");
    return courses;
  }
}

// Fallback courses in case JSON loading fails
function getFallbackCourses() {
  return [
    {
      id: 1,
      title: "JavaScript Fundamentals",
      description:
        "Master the basics of JavaScript programming with hands-on exercises and real-world projects.",
      icon: "🚀",
      duration: "6 weeks",
      lessons: 24,
      completed: false,
      detailedDescription:
        "This comprehensive course covers everything you need to know about JavaScript, from variables and functions to advanced concepts like closures and async programming.",
      lessonsList: [
        { title: "Introduction to JavaScript", duration: "15 min" },
        { title: "Variables and Data Types", duration: "20 min" },
        { title: "Functions and Scope", duration: "25 min" },
        { title: "Objects and Arrays", duration: "30 min" },
        { title: "DOM Manipulation", duration: "35 min" },
        { title: "Event Handling", duration: "20 min" },
        { title: "Async JavaScript", duration: "40 min" },
        { title: "Error Handling", duration: "25 min" },
      ],
    },
    {
      id: 2,
      title: "React Development",
      description:
        "Build modern web applications with React, including hooks, state management, and component architecture.",
      icon: "⚛️",
      duration: "8 weeks",
      lessons: 32,
      completed: false,
      detailedDescription:
        "Learn to build scalable React applications with modern best practices. This course covers components, hooks, state management, routing, and testing.",
      lessonsList: [
        { title: "React Basics", duration: "20 min" },
        { title: "JSX and Components", duration: "25 min" },
        { title: "Props and State", duration: "30 min" },
        { title: "Event Handling in React", duration: "20 min" },
        { title: "React Hooks", duration: "45 min" },
        { title: "Context API", duration: "35 min" },
        { title: "React Router", duration: "30 min" },
        { title: "Testing React Apps", duration: "40 min" },
      ],
    },
    {
      id: 3,
      title: "CSS Grid & Flexbox",
      description:
        "Master modern CSS layout techniques to create responsive and beautiful web designs.",
      icon: "🎨",
      duration: "4 weeks",
      lessons: 16,
      completed: false,
      detailedDescription:
        "Become proficient in CSS Grid and Flexbox to create complex, responsive layouts with ease. Learn when and how to use each layout method effectively.",
      lessonsList: [
        { title: "CSS Flexbox Basics", duration: "25 min" },
        { title: "Flex Properties", duration: "30 min" },
        { title: "CSS Grid Introduction", duration: "20 min" },
        { title: "Grid Template Areas", duration: "35 min" },
        { title: "Responsive Design", duration: "40 min" },
        { title: "Grid vs Flexbox", duration: "25 min" },
        { title: "Advanced Grid Techniques", duration: "45 min" },
        { title: "Real-world Projects", duration: "60 min" },
      ],
    },
    {
      id: 4,
      title: "Node.js Backend",
      description:
        "Learn server-side development with Node.js, Express, and database integration.",
      icon: "🔧",
      duration: "10 weeks",
      lessons: 40,
      completed: false,
      detailedDescription:
        "Build robust backend applications with Node.js and Express. Learn about APIs, databases, authentication, and deployment strategies.",
      lessonsList: [
        { title: "Node.js Fundamentals", duration: "30 min" },
        { title: "Express.js Setup", duration: "25 min" },
        { title: "Routing and Middleware", duration: "35 min" },
        { title: "Database Integration", duration: "45 min" },
        { title: "Authentication & Security", duration: "50 min" },
        { title: "API Development", duration: "40 min" },
        { title: "Testing APIs", duration: "35 min" },
        { title: "Deployment", duration: "30 min" },
      ],
    },
    {
      id: 5,
      title: "Python for Data Science",
      description:
        "Learn Python programming with a focus on data analysis, visualization, and machine learning basics.",
      icon: "🐍",
      duration: "12 weeks",
      lessons: 48,
      completed: false,
      detailedDescription:
        "Master Python for data science with hands-on projects using pandas, numpy, matplotlib, and scikit-learn. Perfect for beginners and professionals looking to transition into data science.",
      lessonsList: [
        { title: "Python Basics", duration: "25 min" },
        { title: "Data Types and Structures", duration: "30 min" },
        { title: "NumPy Fundamentals", duration: "35 min" },
        { title: "Pandas for Data Analysis", duration: "45 min" },
        { title: "Data Visualization with Matplotlib", duration: "40 min" },
        { title: "Statistical Analysis", duration: "50 min" },
        { title: "Machine Learning Basics", duration: "60 min" },
        { title: "Real-world Data Projects", duration: "75 min" },
      ],
    },
    {
      id: 6,
      title: "UI/UX Design Principles",
      description:
        "Master the fundamentals of user interface and user experience design with practical projects.",
      icon: "🎯",
      duration: "7 weeks",
      lessons: 28,
      completed: false,
      detailedDescription:
        "Learn design thinking, user research, wireframing, prototyping, and visual design principles. Create stunning user interfaces that provide excellent user experiences.",
      lessonsList: [
        { title: "Design Thinking Process", duration: "30 min" },
        { title: "User Research Methods", duration: "35 min" },
        { title: "Information Architecture", duration: "25 min" },
        { title: "Wireframing Techniques", duration: "40 min" },
        { title: "Visual Design Principles", duration: "45 min" },
        { title: "Prototyping Tools", duration: "35 min" },
        { title: "Usability Testing", duration: "30 min" },
        { title: "Design Systems", duration: "50 min" },
      ],
    },
  ];
}

// DOM elements
const homePage = document.getElementById("home-page");
const coursePage = document.getElementById("course-page");
const loginPage = document.getElementById("login-page");
const registerPage = document.getElementById("register-page");
const coursesGrid = document.getElementById("courses-grid");
const courseDetail = document.getElementById("course-detail");
const authSection = document.getElementById("auth-section");
const userSection = document.getElementById("user-section");
const welcomeText = document.getElementById("welcome-text");

// Current user state
let currentUser = null;

// Initialize the app
document.addEventListener("DOMContentLoaded", async function () {
  // Show loading state
  showLoadingState();

  // Check if running from file:// protocol
  if (window.location.protocol === "file:") {
    console.log("Running from file:// protocol - using fallback courses");
    showInfoMessage(
      "Running in offline mode. For full functionality, please serve this from a local server."
    );
  }

  // Load courses from JSON file
  await loadCoursesData();

  // Load completion status and auth status
  loadCompletionStatus();
  checkAuthStatus();

  // Hide loading and show courses
  hideLoadingState();
  loadCourses();
});

// Load courses from localStorage or use default
function loadCompletionStatus() {
  const savedStatus = localStorage.getItem("courseCompletions");
  if (savedStatus) {
    const completions = JSON.parse(savedStatus);
    courses.forEach((course) => {
      if (completions[course.id]) {
        course.completed = true;
      }
    });
  }
}

// Save completion status to localStorage
function saveCompletionStatus() {
  const completions = {};
  courses.forEach((course) => {
    if (course.completed) {
      completions[course.id] = true;
    }
  });
  localStorage.setItem("courseCompletions", JSON.stringify(completions));
}

// Render courses on home page
function loadCourses() {
  console.log("Loading courses, total:", courses.length);
  coursesGrid.innerHTML = "";

  if (courses.length === 0) {
    coursesGrid.innerHTML = `
      <div class="error-container">
        <div class="error-icon">📚</div>
        <h3 class="error-title">No courses available</h3>
        <p class="error-message">Courses are being loaded. Please wait a moment.</p>
      </div>
    `;
    return;
  }

  courses.forEach((course) => {
    const courseCard = document.createElement("div");
    courseCard.className = "course-card";
    courseCard.onclick = () => showCourse(course.id);

    courseCard.innerHTML = `
            <div class="course-image">
                <span>${course.icon}</span>
                ${
                  course.completed
                    ? '<div class="completion-badge">Completed</div>'
                    : ""
                }
            </div>
            <div class="course-content">
                <h3 class="course-title">${course.title}</h3>
                <p class="course-description">${course.description}</p>
                <div class="course-meta">
                    <div class="course-duration">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12,6 12,12 16,14"/>
                        </svg>
                        ${course.duration}
                    </div>
                    <div class="course-lessons">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                        </svg>
                        ${course.lessons} lessons
                    </div>
                </div>
            </div>
        `;

    coursesGrid.appendChild(courseCard);
  });
}

// Show course detail page
function showCourse(courseId) {
  const course = courses.find((c) => c.id === courseId);
  if (!course) return;

  courseDetail.innerHTML = `
        <div class="course-header">
            <div class="course-hero-image">
                <span>${course.icon}</span>
            </div>
            <div class="course-info">
                <h1>${course.title}</h1>
                <p>${course.detailedDescription}</p>
                <div class="course-stats">
                    <div class="stat">
                        <div class="stat-number">${course.duration}</div>
                        <div class="stat-label">Duration</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">${course.lessons}</div>
                        <div class="stat-label">Lessons</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">${
                          course.completed ? "Completed" : "In Progress"
                        }</div>
                        <div class="stat-label">Status</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="lessons-section">
            <h2>Course Content</h2>
            <ul class="lessons-list">
                ${course.lessonsList
                  .map(
                    (lesson, index) => `
                    <li class="lesson-item">
                        <div class="lesson-number">${index + 1}</div>
                        <div class="lesson-title">${lesson.title}</div>
                        <div class="lesson-duration">${lesson.duration}</div>
                    </li>
                `
                  )
                  .join("")}
            </ul>
        </div>
        
        <button class="complete-btn ${course.completed ? "completed" : ""}" 
                onclick="toggleCourseCompletion(${course.id})"
                ${course.completed ? "disabled" : ""}>
            ${course.completed ? "✓ Course Completed" : "Mark as Completed"}
        </button>
    `;

  homePage.classList.remove("active");
  coursePage.classList.add("active");
}

// Show home page
function showHome() {
  coursePage.classList.remove("active");
  homePage.classList.add("active");
  loadCourses(); // Refresh courses to show updated completion status
}

// Toggle course completion
function toggleCourseCompletion(courseId) {
  const course = courses.find((c) => c.id === courseId);
  if (!course || course.completed) return;

  // Add completion animation
  const button = event.target;
  button.style.transform = "scale(0.95)";
  button.innerHTML = "Completing...";

  setTimeout(() => {
    course.completed = true;
    saveCompletionStatus();

    button.innerHTML = "✓ Course Completed";
    button.classList.add("completed");
    button.disabled = true;
    button.style.transform = "scale(1)";

    // Update the stats section
    const statElements = document.querySelectorAll(".stat-number");
    if (statElements.length >= 3) {
      statElements[2].textContent = "Completed";
    }

    // Show success message
    showSuccessMessage();
  }, 1000);
}

// Show success message
function showSuccessMessage() {
  const message = document.createElement("div");
  message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        z-index: 1000;
        font-weight: 500;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
  message.innerHTML = "🎉 Congratulations! Course completed successfully!";

  document.body.appendChild(message);

  // Animate in
  setTimeout(() => {
    message.style.transform = "translateX(0)";
  }, 100);

  // Remove after 3 seconds
  setTimeout(() => {
    message.style.transform = "translateX(100%)";
    setTimeout(() => {
      document.body.removeChild(message);
    }, 300);
  }, 3000);
}

// Add some interactive animations
document.addEventListener("mouseover", function (e) {
  if (e.target.classList.contains("course-card")) {
    e.target.style.transform = "translateY(-8px) scale(1.02)";
  }
});

document.addEventListener("mouseout", function (e) {
  if (e.target.classList.contains("course-card")) {
    e.target.style.transform = "translateY(0) scale(1)";
  }
});

// Add keyboard navigation
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && coursePage.classList.contains("active")) {
    showHome();
  }
});
// Authentication Functions

// Check if user is logged in
function checkAuthStatus() {
  const savedUser = localStorage.getItem("currentUser");
  if (savedUser) {
    currentUser = JSON.parse(savedUser);
    updateAuthUI();
  }
}

// Update authentication UI
function updateAuthUI() {
  if (currentUser) {
    authSection.style.display = "none";
    userSection.style.display = "flex";
    welcomeText.textContent = `Welcome, ${currentUser.name}!`;
  } else {
    authSection.style.display = "flex";
    userSection.style.display = "none";
  }
}

// Show login page
function showLogin() {
  hideAllPages();
  loginPage.classList.add("active");
}

// Show register page
function showRegister() {
  hideAllPages();
  registerPage.classList.add("active");
}

// Hide all pages
function hideAllPages() {
  homePage.classList.remove("active");
  coursePage.classList.remove("active");
  loginPage.classList.remove("active");
  registerPage.classList.remove("active");
}

// Handle login form submission
function handleLogin(event) {
  event.preventDefault();

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  // Get registered users from localStorage
  const users = JSON.parse(localStorage.getItem("registeredUsers") || "[]");

  // Find user with matching credentials
  const user = users.find((u) => u.email === email && u.password === password);

  if (user) {
    // Login successful
    currentUser = { id: user.id, name: user.name, email: user.email };
    localStorage.setItem("currentUser", JSON.stringify(currentUser));

    showMessage("Login successful! Welcome back.", "success");

    setTimeout(() => {
      updateAuthUI();
      showHome();
    }, 1500);
  } else {
    // Login failed
    showMessage("Invalid email or password. Please try again.", "error");
  }
}

// Handle register form submission
function handleRegister(event) {
  event.preventDefault();

  const name = document.getElementById("register-name").value;
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;
  const confirmPassword = document.getElementById(
    "register-confirm-password"
  ).value;

  // Validation
  if (password !== confirmPassword) {
    showMessage("Passwords do not match. Please try again.", "error");
    return;
  }

  if (password.length < 6) {
    showMessage("Password must be at least 6 characters long.", "error");
    return;
  }

  // Get existing users
  const users = JSON.parse(localStorage.getItem("registeredUsers") || "[]");

  // Check if email already exists
  if (users.find((u) => u.email === email)) {
    showMessage("An account with this email already exists.", "error");
    return;
  }

  // Create new user
  const newUser = {
    id: Date.now(),
    name: name,
    email: email,
    password: password,
    registeredAt: new Date().toISOString(),
  };

  // Save user
  users.push(newUser);
  localStorage.setItem("registeredUsers", JSON.stringify(users));

  // Auto-login the new user
  currentUser = { id: newUser.id, name: newUser.name, email: newUser.email };
  localStorage.setItem("currentUser", JSON.stringify(currentUser));

  showMessage("Account created successfully! Welcome to LearnHub.", "success");

  setTimeout(() => {
    updateAuthUI();
    showHome();
  }, 1500);
}

// Logout function
function logout() {
  currentUser = null;
  localStorage.removeItem("currentUser");
  updateAuthUI();
  showHome();
  showMessage("You have been logged out successfully.", "success");
}

// Show message function
function showMessage(text, type) {
  // Remove existing messages
  const existingMessages = document.querySelectorAll(".message");
  existingMessages.forEach((msg) => msg.remove());

  const message = document.createElement("div");
  message.className = `message ${type}`;
  message.textContent = text;

  // Insert message at the top of the active form
  const activeForm = document.querySelector(".page.active .auth-form form");
  if (activeForm) {
    activeForm.insertBefore(message, activeForm.firstChild);

    // Auto-remove message after 5 seconds
    setTimeout(() => {
      if (message.parentNode) {
        message.remove();
      }
    }, 5000);
  }
}

// Update the showHome function to handle authentication pages
function showHome() {
  hideAllPages();
  homePage.classList.add("active");
  loadCourses(); // Refresh courses to show updated completion status
}

// Update keyboard navigation to handle auth pages
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    if (coursePage.classList.contains("active")) {
      showHome();
    } else if (
      loginPage.classList.contains("active") ||
      registerPage.classList.contains("active")
    ) {
      showHome();
    }
  }
});

// Add form validation styling
document.addEventListener("input", function (e) {
  if (e.target.tagName === "INPUT") {
    if (e.target.checkValidity()) {
      e.target.style.borderColor = "#10b981";
    } else {
      e.target.style.borderColor = "#ef4444";
    }
  }
});

// Reset form styling on focus
document.addEventListener(
  "focus",
  function (e) {
    if (e.target.tagName === "INPUT") {
      e.target.style.borderColor = "#667eea";
    }
  },
  true
);
// Loading state functions
function showLoadingState() {
  coursesGrid.innerHTML = `
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading courses...</p>
    </div>
  `;
}

function hideLoadingState() {
  const loadingContainer = document.querySelector(".loading-container");
  if (loadingContainer) {
    loadingContainer.remove();
  }
}

// Error message function (not used anymore since we have fallback)
function showErrorMessage(message) {
  console.warn("Course loading issue:", message);
  // We don't show error UI anymore since we have fallback courses
}
// Show info message
function showInfoMessage(message) {
  const infoDiv = document.createElement("div");
  infoDiv.style.cssText = `
    position: fixed;
    top: 70px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    z-index: 1000;
    font-size: 0.9rem;
    max-width: 90%;
    text-align: center;
  `;
  infoDiv.innerHTML = `ℹ️ ${message}`;

  document.body.appendChild(infoDiv);

  // Remove after 5 seconds
  setTimeout(() => {
    if (infoDiv.parentNode) {
      infoDiv.remove();
    }
  }, 5000);
}
