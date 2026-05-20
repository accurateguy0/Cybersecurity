In the previous task, we set our variables and constants; moreover, we picked a random `secret` number for the user to guess. Now, we need to prompt the user to take a guess and enter a number. In the first line, we wait for the user to input a value and save it in `text`. In the second line, we parse the `text` as an integer of base `10` using `parseInt(text, 10)`. The `parseInt()` method takes the user input and converts it from text into an integer value.

```javascript
const text = await rl.question("Take a guess: ");
guess = parseInt(text, 10);
```

Optional Notes  

The `await` instruction pauses the system until the user responds. Obviously, Node.js’s default behavior is not to wait for a user to enter a value. Remember that Node.js is built as a runtime environment for web applications, not to run such a command-line JavaScript program. Consequently, we need to use libraries to override the default behavior and force Node.js to wait for the user. The following lines achieve this:

```javascript
import * as readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

const rl = readline.createInterface({ input, output });
```

The first line borrows (`import`) the `readline` module so that the program can ask questions and wait for typed answers. The `/promises` part means it can “pause” neatly until the user responds. The second line imports two more modules, `stdin`, short for standard input (usually the keyboard), and `stdout`, short for standard output (usually the screen); moreover, it renames them to `input` and `output` respectively. The third line sets up the conversation channel using the “microphone” from line 1 and the “wires” from line 2.

Why is this so complicated to get command-line input? Because we are using Node.js to test our JavaScript program, we do not need to keep the server busy waiting for user input. Deviating from the expected default requires us to add these extra library imports.

## Clean Execution

To read user input, we had to create an interface we likened to a microphone. Before the program finishes, we need to close this interface. You would also switch off your microphone after the Q&A session. To close the interface, we use `rl.close()`. As a result, our code will declare and initialize the `rl` (short for readline), use it to get `text` input from the user, and `close()` it. These three steps are shown below.

```javascript
const rl = readline.createInterface({ input, output });

try {
//...
    const text = await rl.question("Take a guess: "); // rl.question() returns text (a string)
//...
} finally {
    rl.close();
}
```

The `try` block creates a safe environment so that if something goes wrong, the program won’t crash. Think of it as `try`ing to run a set of statements, and if something happens, handle it gracefully, and `finally` clean up.

Let’s summarize what we are doing:

1. We are importing the `readline` module with the `/promises` part, indicating that the script will handle waiting without freezing everything
2. Then we imported `stdout` (standard output) and `stdin` (standard input) as `input` and `output`
3. Using these imported modules, we create the readline `const` with the name `rl`.
4. The program makes its guess using `Math.random()` and saves that as `secret`, a constant.
5. We declared two variables, `tries` and `guess`
6. We displayed on the screen that “_a number between 1 and 20_” has been selected
7. The user’s response is considered a guess and will be saved in `text`, a constant
8. The user’s response is converted to a number using `parseInt()`
9. The number of `tries` increases by one
10. Finally, we clean up and close the readline interface, `rl`, that we created earlier

## Putting it All Together

The first draft we have built so far is listed below and is also available on the system as `guess_v1.js`, which can be found in the `/home/ubuntu/JavaScript-Demo` directory.

```javascript
import * as readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

const rl = readline.createInterface({ input, output });

try {
    const secret = Math.floor(Math.random() * (20)) + 1; // 1 <= secret <= 20
    let tries = 0;
    let guess = 0; // start with a value that cannot be the secret (since secret is 1..20)

    console.log("I'm thinking of a number between 1 and 20");

    const text = await rl.question("Take a guess: "); // rl.question() returns text (a string)
    guess = parseInt(text, 10); // convert the text to a number

    tries = tries + 1; // add 1 try

} finally {
    rl.close();
}
```

```javascript
// Give a hint using if / else if / else.
if (guess < 1 || guess > 20) {
    console.log("That number is out of range. Try again.");
} else if (guess < secret) {
    console.log("Too low, try again.");
} else if (guess > secret) {
    console.log("Too high, try again.");
} else {
    console.log("You got it in", tries, "tries!");
}
```
```javascript
// Repeat until the user guesses the secret number.
while (guess !== secret) {
    const text = await rl.question("Take a guess: "); // rl.question() returns text (a string)
    guess = parseInt(text, 10); // convert the text to a number

    tries = tries + 1; // add 1 try

    // Give a hint using if / else if / else.
    if (guess < 1 || guess > 20) {
        console.log("That number is out of range. Try again.");
    } else if (guess < secret) {
        console.log("Too low, try again.");
    } else if (guess > secret) {
        console.log("Too high, try again.");
    } else {
        console.log("You got it in", tries, "tries!");
    }
}
```
