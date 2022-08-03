// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v3.0.0/contracts/token/ERC721/ERC721.sol";

contract Auctions is ERC721 {
    using SafeMath for uint;

    constructor() ERC721("Auctions", "AUC") public {}

    struct Token {
        address creator;
        address beneficiary;
        string name;
        string description;
    
        bool auctionComplete;
        uint auctionEndTime;
        uint minimumBid;
        uint newBidderFee;
        uint highestBid;
        uint newBidderFees;

        address[] bidders;
        mapping(address => uint) bids;
        mapping(address => uint) balances;

        address highestBidder;
    }

    mapping(uint => Token) public tokenCollection;
    event bids(uint tokenId, address bidder, uint256 bid);
    
    function createToken(string memory name, string memory description, uint minimumBid, uint newBidderFee;, uint auctionEndTime, address beneficiary, string memory tokenURI) public {
        require(auctionEndTime >= block.timestamp);

        uint256 tokenId = totalSupply();
        _mint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);

        address[] storage bidders;
        bidders.push(msg.sender);

        tokenCollection[tokenId] = Token(msg.sender, beneficiary, name, description, false, auctionEndTime, minimumBid, newBidderFee, 0, bidders, msg.sender);
    }

    modifier ends(uint tokenId) {
        require(tokenCollection[tokenId].auctionComplete == false);

        Token storage token = tokenCollection[tokenId];

        if (block.timestamp >= token.auctionEndTime) {
            uint _highestBid = 0;

            for (uint i = 0; i < token.bidders.length; i++) {
                if (token.bids[token.bidders[i]] > _highestBid) {
                    token.highestBid = token.bids[token.bidders[i]];
                    token.highestBidder = token.bidders[i];
                }
            }

            payable(token.beneficiary).transfer(token.highestBid + newBidderFees);
            token.balances[token.highestBidder] = 0;

            _transfer(token.creator, token.highestBidder, tokenId);

            for (uint i = 0; i < token.bidders.length; i++) {
                address payable bidder = payable(token.bidders[i]);
                bidder.transfer(token.balances[bidder]);
                token.balances[bidder] = 0;
            }

            token.auctionComplete = true;
        }

        require(token.auctionComplete == false);
        _;
    }

    function claimEnd(uint tokenID) ends(tokenID) public {}

    function firstBid(address bidder, uint tokenId) public view returns(bool) {
        Token storage token = tokenCollection[tokenId];

        for (uint i = 0; i < token.bidders.length; i++) {
            if (token.bidders[i] == bidder) {
                return false;
            }
        }

        return true;
    }

    function updateBid(uint tokenId, uint bid) public payable ends(tokenId) {
        Token storage token = tokenCollection[tokenId];

        if (firstBid(msg.sender, tokenId) == true) {
            require(bid > 0 && msg.value == bid && msg.value >= token.minimumBid + token.newBidderFee);
            token.bids[msg.sender] = bid;
            token.balances[msg.sender] = bid;
            token.bidders.push(msg.sender);
            token.newBidderFees += bid / token.newBidderFees;
        }

        uint senderBalance = token.balances[msg.sender];
        uint balanceDifference = (bid - senderBalance);

        if (bid > senderBalance) {
            require(msg.value == balanceDifference);
            token.bids[msg.sender] = bid;
            token.balances[msg.sender] += balanceDifference;
        } else {
            token.bids[msg.sender] = bid;
        }
        
        emit bids(tokenId, msg.sender, bid);
    }

    function withdrawDifference (uint tokenId) public ends(tokenId) {
        Token storage token = tokenCollection[tokenId];

        uint senderBid = token.bids[msg.sender];
        uint senderBalance = token.balances[msg.sender];
    
        require(senderBalance > senderBid);
        uint balanceDifference = senderBalance - senderBid;

        msg.sender.transfer(balanceDifference);
        token.balances[msg.sender] -= balanceDifference;
    }

    function exitAuction(uint tokenId) public ends(tokenId) {
        Token storage token = tokenCollection[tokenId];

        msg.sender.transfer(token.balances[msg.sender]);
        token.balances[msg.sender] = 0;
        token.bids[msg.sender] = 0;
    }

    function viewToken(uint tokenId) public view returns(address, string memory, string memory, bool, uint, uint, address) {
        Token storage token = tokenCollection[tokenId];

        return (token.creator, token.name, token.description, token.auctionComplete, token.auctionEndTime, token.highestBid, token.beneficiary);
    }

    function viewHighestBid(uint tokenId) public view returns(uint) {
        uint _highestBid = 0;
        for (uint i = 0; i < token.bidders.length; i++) {
            if (token.bids[token.bidders[i]] > _highestBid) {
                _highestBid = token.bids[token.bidders[i]];
            }
        }

        return _highestBid;
    }

    function viewHighestBidder(uint tokenId) public view returns(uint) {
        uint _highestBidder = 0;
        for (uint i = 0; i < token.bidders.length; i++) {
            if (token.bids[token.bidders[i]] > _highestBid) {
                _highestBidder = token.bidders[i];
            }
        }

        return _highestBidder;
    }

    function viewCurrentBid(uint tokenId) public view returns(uint) {
        return tokenCollection[tokenId].bids[msg.sender];
    }

    function viewCurrentBalance(uint tokenId) public view returns(uint) {
        return tokenCollection[tokenId].balances[msg.sender];
    }
}

// Creator changing minimumBid and biddingFee after auction begins.
