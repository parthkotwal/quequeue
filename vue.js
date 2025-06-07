// VARIABLES AND SCOPE
// ------------------------
let b = 2;
const c = 3;

// Notes
// Never use var
// let for local mutations
// const for props (mechanism for passing data from parent to child component)
// Example prop:
function Parent() {
    const message = "Hello!";
    return (
        <Child text={message}/>
    );
}

function Child(props){
    return (
        <p>{props.text}</p>
    );
}


// FUNCTIONS
// ------------------------

function add1(x, y) {
    return x+y;
}
const add2 = (x,y) => x+y;

const obj = {
    value: 42,

    // Traditional
    // Have their own 'this' context, which is determined by how function is called
    sayTraditional: function() {
        console.log(this.value); // 42
    },


    // Arrow
    // Inherit 'this' from surrounding scope
    sayArrow: () => {
        console.log(this.value); // undefined since 'this' is not bounded
    }

};


// OBJECTS
// ------------------------

// Object literals
const user = {
    name: "Jane",
    age: 30,
};

// Destructuring - allows for extracting values from arrays or objects and assigning them to variables in a concise way.
const {name, age} = user


// PROMISES & ASYNC/AWAIT
// ------------------------
// JS is asynchronous by default - runs in single threat but doesn't block for long tasks
// Promise - JS object that represents eventual result of an asynchronous operation. Three results:
    // pending - still happening
    // fulfilled - successful
    // rejected - failed

fetch('/api/user')
  .then(response => {
    if (!response.ok) throw new Error("Network error");
    return response.json();
  })
  .then(data => {
    console.log("User data:", data);
    return fetch(`/api/posts?user=${data.id}`);
  })
  .then(postsRes => postsRes.json())
  .then(posts => {
    console.log("User posts:", posts);
  })
  .catch(error => {
    console.error("Something went wrong:", error);
  });

async function loadUserData() {
    try{
        const response = await fetch('/api/user');
        if (!response.ok) throw new Error("Network error");

        const data = await response.json();
        console.log("User data:", data);

        const postsRes = await fetch(`/api/posts?user=${data.id}`);
        const posts = await postsRes.json();
        console.log("User posts:", posts);
    }
    catch (error) {
        console.error("Error:", error);
    }
}

// Spread
const base = {name:"Alice"};
const extended = { ...base, location:"NY"};

// Rest
function sum(...args) {
    return args.reduce((a, b) )
}

