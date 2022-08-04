// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v3.0.0/contracts/token/ERC721/ERC721.sol";

contract Auctions is ERC721 {
    using SafeMath for uint;

    constructor() ERC721("Auctions", "AUC") public {}

    struct Token {
        address creator;
        string name;
        string description;
        address beneficiary;    
    
        bool auctionComplete;
        uint auctionEndTime;
        uint highestBid;
        address highestBidder;

        mapping(address => uint) balances;
    }

    mapping(uint => Token) public tokenCollection;
    event bids(uint tokenId, address bidder, uint256 bid);
    
    function createToken(string memory name, string memory description, address beneficiary, uint auctionEndTime, string memory tokenURI) public {
        require(auctionEndTime >= block.timestamp);

        uint256 tokenId = totalSupply();
        _mint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);

        tokenCollection[tokenId] = Token(msg.sender, beneficiary, name, description, false, auctionEndTime, 0, msg.sender);
    }

    modifier ends(uint tokenId) {
        require(tokenCollection[tokenId].auctionComplete == false);

        if (block.timestamp >= tokenCollection[tokenId].auctionEndTime) {
            Token storage token = tokenCollection[tokenId];
            
            payable(token.beneficiary).transfer(token.highestBid);
            token.balances[token.highestBidder] = 0;

            token.auctionComplete = true;
        }

        require(token.auctionComplete == false);
        _;
    }

    function claimEnd(uint tokenID) ends(tokenID) public {}

    function placeBid(uint tokenId, uint bid) public payable ends(tokenId) {
        if (bid > tokenCollection[tokenId].highestBid) {
            Token storage token = tokenCollection[tokenId];
            
            uint senderBalance = token.balances[msg.sender];
            uint balanceDifference = (bid - senderBalance);

            require(msg.value == balanceDifference);
            token.balances[msg.sender] += balanceDifference;
            token.highestBid = bid;
            token.highestBidder = msg.sender;
        
            emit bids(tokenId, msg.sender, bid);}
    }

    function withdraw (uint tokenId) public ends(tokenId) {
        require(msg.sender != tokenCollection[tokenId].highestBidder);
        require(tokenCollection[tokenId].balances[msg.sender] > 0);

        Token storage token = tokenCollection[tokenId];

        uint senderBalance = token.balances[msg.sender];

        msg.sender.transfer(senderBalance);
        token.balances[msg.sender] = 0;
    }

    function viewToken(uint tokenId) public view returns(address, string memory, string memory, bool, uint, uint, address) {
        Token storage token = tokenCollection[tokenId];

        return (token.creator, token.name, token.description, token.beneficiary, token.auctionComplete, token.auctionEndTime, token.highestBid, token.highestBidder);
    }

    function viewCurrentBalance(uint tokenId) public view returns(uint) {
        return tokenCollection[tokenId].balances[msg.sender];
    }
}

