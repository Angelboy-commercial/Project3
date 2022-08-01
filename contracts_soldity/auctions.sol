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
    
        bool auctionComplete;
        uint auctionEndTime;
        uint highestBid;

        address[] bidders;
        mapping(address => uint) bids;
        mapping(address => uint) balances;

        address highestBidder;
        address beneficiary;
    }

    mapping(uint => Token) public tokenCollection;
    event bids(address bidder, uint256 bid);
    
    modifier ends(uint tokenId) {
        require(tokenCollection[tokenId].auctionComplete == false);

        if (block.timestamp >= tokenCollection[tokenId].auctionEndTime) {
            payable(tokenCollection[tokenId].beneficiary).transfer(tokenCollection[tokenId].highestBid);
            tokenCollection[tokenId].balances[tokenCollection[tokenId].highestBidder] = 0;

            _transfer(address(this), tokenCollection[tokenId].highestBidder, tokenId);

            for (uint i = 0; i < tokenCollection[tokenId].bidders.length; i++) {
                address payable bidder = payable(tokenCollection[tokenId].bidders[i]);
                bidder.transfer(tokenCollection[tokenId].balances[bidder]);
                tokenCollection[tokenId].balances[bidder] = 0;
            }

            tokenCollection[tokenId].auctionComplete = true;
        }

        require(tokenCollection[tokenId].auctionComplete == false);
        _;
    }

    function createToken(string memory name, string memory description, uint startingBid, uint auctionEndTime, address beneficiary, string memory tokenURI) public {
        require(auctionEndTime >= block.timestamp);

        uint256 tokenId = totalSupply();
        _mint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);

        address[] storage bidders;
        bidders.push(msg.sender);

        tokenCollection[tokenId] = Token(msg.sender, name, description, false, auctionEndTime, startingBid, bidders, msg.sender, beneficiary);
    }

    function claimEnd(uint tokenID) ends(tokenID) public {}

    function firstBid(address bidder, uint tokenId) public view returns(bool) {
        for (uint i = 0; i < tokenCollection[tokenId].bidders.length; i++) {
            if (tokenCollection[tokenId].bidders[i] == bidder) {
                return false;
            } else {
                return true;
            }
        }
    }

    function updateBid(uint tokenId, uint bid) public payable ends(tokenId) {
        if (firstBid(msg.sender, tokenId) == true) {
            require(bid > 0 && msg.value == bid);
            tokenCollection[tokenId].bids[msg.sender] = bid;
            tokenCollection[tokenId].balances[msg.sender] = bid;
            tokenCollection[tokenId].bidders.push(msg.sender);
        }

        uint senderBalance = tokenCollection[tokenId].balances[msg.sender];
        uint balanceDifference = (bid - senderBalance);

        if (bid >= senderBalance) { //
            require(msg.value == balanceDifference);
            tokenCollection[tokenId].bids[msg.sender] = bid;
            tokenCollection[tokenId].balances[msg.sender] += balanceDifference;
        } else {
            tokenCollection[tokenId].bids[msg.sender] = bid;
        }

        uint _highestBid = bid - 1;
        tokenCollection[tokenId].highestBidder = msg.sender;
        for (uint i = 0; i < tokenCollection[tokenId].bidders.length; i++) {
            if (tokenCollection[tokenId].bids[tokenCollection[tokenId].bidders[i]] > _highestBid) {
                _highestBid = tokenCollection[tokenId].bids[tokenCollection[tokenId].bidders[i]];
                tokenCollection[tokenId].highestBidder = tokenCollection[tokenId].bidders[i];
            }
        }

        tokenCollection[tokenId].highestBid = _highestBid;

        emit bids(msg.sender, bid);
    }

    function withdrawDifference (uint tokenId) public ends(tokenId) {
        uint senderBid = tokenCollection[tokenId].bids[msg.sender];
        uint senderBalance = tokenCollection[tokenId].balances[msg.sender];
    
        require(senderBalance > senderBid);
        uint balanceDifference = senderBalance - senderBid;

        msg.sender.transfer(balanceDifference);
        tokenCollection[tokenId].balances[msg.sender] -= balanceDifference;
    }

    function exitAuction(uint tokenId) public ends(tokenId) {
        msg.sender.transfer(tokenCollection[tokenId].balances[msg.sender]);
        tokenCollection[tokenId].balances[msg.sender] = 0;
        tokenCollection[tokenId].bids[msg.sender] = 0;

        uint _highestBid = 0;
        for (uint i = 0; i < tokenCollection[tokenId].bidders.length; i++) {
            if (tokenCollection[tokenId].bids[tokenCollection[tokenId].bidders[i]] > _highestBid) {
                _highestBid = tokenCollection[tokenId].bids[tokenCollection[tokenId].bidders[i]];
                tokenCollection[tokenId].highestBidder = tokenCollection[tokenId].bidders[i];
            }
        }

        tokenCollection[tokenId].highestBid = _highestBid;
    }

    function viewToken(uint tokenId) public view returns(address, string memory, string memory, bool, uint, uint, address) {
        return (tokenCollection[tokenId].creator,
               tokenCollection[tokenId].name,
               tokenCollection[tokenId].description,
               tokenCollection[tokenId].auctionComplete,
               tokenCollection[tokenId].auctionEndTime,
               tokenCollection[tokenId].highestBid,
               tokenCollection[tokenId].beneficiary);
    }

    function viewHighestBid(uint tokenId) public view returns(uint) {
        return tokenCollection[tokenId].highestBid;
    }

    function viewCurrentBid(uint tokenId) public view returns(uint) {
        return tokenCollection[tokenId].bids[msg.sender];
    }

    function viewCurrentBalance(uint tokenId) public view returns(uint) {
        return tokenCollection[tokenId].balances[msg.sender];
    }
}
