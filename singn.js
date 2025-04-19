import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyBeKxOK5czjXeqF_PtwiUGuvCyKRKNo7WY",
  authDomain: "create-account-21a9a.firebaseapp.com",
  projectId: "create-account-21a9a",
  storageBucket: "create-account-21a9a.firebasestorage.app",
  messagingSenderId: "332433901718",
  appId: "1:332433901718:web:b41337d1a7d487b2385ab7",
  measurementId: "G-2T86XSY0JL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);  // Added app parameter here
const db = getFirestore(app);

const submit = document.getElementById("submit");

submit.addEventListener('click', function (event) {
  event.preventDefault();

  // Input fields
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const idNumber = document.getElementById("idNumber").value;
  const school = document.getElementById("school").value;
  const password = document.getElementById("password").value;

  // Basic validation
  if (!username || !email || !idNumber || !school || !password) {
    alert("Please fill in all fields");
    return;
  }

  // Create user with email and password
  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // User created successfully
      const user = userCredential.user;
      
      // Store additional user data in Firestore
      setDoc(doc(db, "users", user.uid), {
        email: user.email,
        uid: user.uid,
        displayName: username,
        idNumber: idNumber,
        school: school,
        createdAt: new Date()  // Adding timestamp for when user was created
      })
      .then(() => {
        alert("Account created successfully!");
        window.location.href = "profile.html";
      })
      .catch((error) => {
        console.error("Error writing document: ", error);
        alert("Account created, but there was an error saving your profile data.");
      });
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      
      // More specific error messages
      if (errorCode === 'auth/email-already-in-use') {
        alert("This email is already registered.");
      } else if (errorCode === 'auth/weak-password') {
        alert("Password should be at least 6 characters.");
      } else if (errorCode === 'auth/invalid-email') {
        alert("Invalid email format.");
      } else {
        alert(errorMessage);
      }
    });
});