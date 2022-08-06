// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v3.0.0/contracts/token/ERC721/ERC721.sol";

contract Auctions is ERC721 {
    using SafeMath for uint;

    constructor() ERC721("Auctions", "AUC") public {}

    struct Auction {
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

    mapping(uint => Auction) public tokenCollection;
    event bids(uint tokenId, address bidder, uint256 bid);
    
    function createToken(string memory name, string memory description, address beneficiary, uint auctionEndTime, string memory tokenURI) public {
        require(auctionEndTime >= block.timestamp, 'End time given has already past.');

        uint256 tokenId = totalSupply();
        _mint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);

        tokenCollection[tokenId] = Auction(msg.sender, name, description, beneficiary, false, auctionEndTime, 0, msg.sender);
    }

    modifier ends(uint tokenId) {
        require(tokenCollection[tokenId].auctionComplete == false, "Auction already ended.");

        if (block.timestamp >= tokenCollection[tokenId].auctionEndTime) {
            Auction storage token = tokenCollection[tokenId];

            payable(token.beneficiary).transfer(token.highestBid);
            token.balances[token.highestBidder] = 0;

            _transfer(token.creator, token.highestBidder, tokenId);

            token.auctionComplete = true;
        }

        _;
    }

    function claimEnd(uint tokenID) ends(tokenID) public {}

    function placeBid(uint tokenId, uint bid) public payable ends(tokenId) {
        require(bid > tokenCollection[tokenId].auctionComplete == false, "Auction already ended.");
        require(bid > tokenCollection[tokenId].highestBid, "Bids placed must exceed highest bid.");

        Auction storage token = tokenCollection[tokenId];
        
        uint senderBalance = token.balances[msg.sender];
        uint balanceDifference = (bid - senderBalance);

        require(msg.value == balanceDifference, 'Transaction value must equal increase over previous bid.');
        token.balances[msg.sender] += balanceDifference;
        token.highestBid = bid;
        token.highestBidder = msg.sender;
    
        emit bids(tokenId, msg.sender, bid);
    }

    function withdraw(uint tokenId) public ends(tokenId) {
        require(msg.sender != tokenCollection[tokenId].highestBidder, "Highest bidder can't withdraw funds.");
        require(tokenCollection[tokenId].balances[msg.sender] > 0, "Sender has zero balance.");

        Auction storage token = tokenCollection[tokenId];

        uint senderBalance = token.balances[msg.sender];

        msg.sender.transfer(senderBalance);
        token.balances[msg.sender] = 0;
    }

    function viewToken(uint tokenId) public view returns(address, string memory, string memory, address, bool, uint, uint, address) {
        Auction storage token = tokenCollection[tokenId];

        return (token.creator, token.name, token.description, token.beneficiary, token.auctionComplete, token.auctionEndTime, token.highestBid, token.highestBidder);
    }

    function viewSenderBalance(uint tokenId) public view returns(uint) {
        Auction storage token = tokenCollection[tokenId];
        uint senderBalance;

        senderBalance = token.balances[msg.sender];

        return senderBalance;
    }
}
