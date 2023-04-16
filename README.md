# blitzclock-micro

This is a Python script that connects your Raspiblitz Fullnode (LND) to a Blockclock micro and retrieves data about your Node. It uses that data to update a Blockclock micro, which displays the current Bitcoin block height, unconfirmed onchain transactions, lighning transactions and other relevant information. The update is performed every 5 minutes by a cronjob.

## Getting Started

To use this script, you'll need:

+ [A Raspiblitz Fullnode with LND running](https://github.com/rootzoll/raspiblitz)
+ [Blockclock Micro](https://blockclockmicro.com)


## Getting Started

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



Provide code examples and explanations of how to get the project, e.g.,

	git clone https://github.com/Jasonnor/README.md.git
    cd README.md
    npm install README.md
    npm start

## Usage

Show how to use the project or library.
    
## License

This project is licensed under the MIT License - see the LICENSE file for details.
