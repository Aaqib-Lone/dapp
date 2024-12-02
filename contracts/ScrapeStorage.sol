// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract ScrapeStorage {
    string public data;
    // Function to store scraped data
    function storeData(string memory _data) public {
        data = _data;
    }
    // Function to retrieve the stored data
    function retrieveData() public view returns (string memory) {
        return data;
    }
}
