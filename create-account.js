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
const auth = getAuth();
const db = getFirestore(app);

const submit = document.getElementById("submit");

submit.addEventListener('click', function (event) {
  event.preventDefault();

  //input fields
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const idNumber = document.getElementById("idNumber").value; // Fixed typo here (.vaiue -> .value)
  const school = document.getElementById("school").value;
  const password = document.getElementById("password").value;

  //create user
  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      setDoc(doc(db, "users", user.uid), {
        email: user.email,
        uid: user.uid,
        displayName: username,
        idNumber: idNumber,
        school: school,
      }).then(() => {
          window.location.href = "profile.html";
        });
    })
    .catch((error) => {
      const errorMessage = error.message;
      alert(errorMessage);
    });
});


