Magic_Test
----------
> Even Magic is all about scientific proof these days, prove your magic powers and defy laws of math ! you can read the source code (http://web2.quals18.ctfsecurinets.com/server.js) to have a better understanding of what i mean.
>
> Link : http://web1.quals18.ctfsecurinets.com

Let's take a look at the web page first.

![MagicTest Page](https://github.com/DancingSimpletons/writeups/blob/master/securinets-2018/MagicTest.PNG)

The server js has this check to get the flag:
``` javascript
var priority = Math.pow(2, getAsciiCode(username) + getTimestamp(birthDay));
    
if(priority >= 0) {
    res.send('Hey peasent, no flag for you !!');
}
else {
    res.send('Your magical powers have been proven, here is your flag: ' + flag );
}
```
Ok, so what does javascripts `Math.pow()` return? [MDN says:](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/pow)
``` javascript
// simple
Math.pow(7, 2);    // 49
Math.pow(7, 3);    // 343
Math.pow(2, 10);   // 1024
// fractional exponents
Math.pow(4, 0.5);  // 2 (square root of 4)
Math.pow(8, 1/3);  // 2 (cube root of 8)
Math.pow(2, 0.5);  // 1.4142135623730951 (square root of 2)
Math.pow(2, 1/3);  // 1.2599210498948732 (cube root of 2)
// signed exponents
Math.pow(7, -2);   // 0.02040816326530612 (1/49)
Math.pow(8, -1/3); // 0.5
// signed bases
Math.pow(-7, 2);   // 49 (squares are positive)
Math.pow(-7, 3);   // -343 (cubes can be negative)
Math.pow(-7, 0.5); // NaN (negative numbers don't have a real square root)
// due to "even" and "odd" roots laying close to each other, 
// and limits in the floating number precision, 
// negative bases with fractional exponents always return NaN
Math.pow(-7, 1/3); // NaN
```
Since we can basically fill in any date, let's give it some data to make `Math.pow()` return NaN.
We can easily check it in the console of our browser by copying the main parts from the server.js

``` javascript
function getTimestamp(date) {
    try{
        var x = Math.floor((new Date(date)) / 1000);
        return x;
    } catch( e ){
        return  Math.floor((new Date()) / 1000);
    }
}

function getAsciiCode(str)
{
    var arr1 = [];
    for (var n = 0; n < str.length; n ++) 
     {
        var ascii = Number(str.charCodeAt(n));
        arr1.push(ascii);
     }
    return arr1.join('');
}
var priority = Math.pow(2, getAsciiCode("HorseEgg") + getTimestamp("1001-01-01"));
console.log(priority);
//Output: NaN
```

Filling in `HorseEgg` as name and `1001-01-01` as birthday on the webpage we get the flag: `Flag{PhP_H4s_seCuriTY_issues_THEY-Said!!!}`
