
//You can run this script directly in your browser's developer tools (F12 -> Console) while on that page. It uses the existing variables and functions to reverse the process:
//code
JavaScript
(function() {
    //  Re-generate the key 'c' exactly as the script does
    let solve_random = Random(0);
    let solve_c = "";
    for(let i=0; i<128; ++i) {
        solve_c += secret[Math.floor(solve_random() * 64 + 39)];
    }
    let key = parseHexString(solve_c);

    //  Decode the target 'flag' from Base64
    let encrypted = atob(flag);
    
    //  XOR the encrypted bytes with the key to get the original flag
    let result = "";
    for(let i=0; i<encrypted.length; ++i) {
        result += String.fromCharCode(encrypted.charCodeAt(i) ^ key[i]);
    }

    console.log("The flag is: " + result);
    alert("The flag is: " + result);
})();