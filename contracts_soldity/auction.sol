pragma solidity ^0.5.0;


contract Auction{
    using SafeMath for uint;
    
    uint256 AuctionTimeLimit;
    address highest_bidder;
    uint256 highest_bid;
    event Bid(address bidder, uint256 amount);

    constructor(uint8 AuctionDayLength_, uint256 startingBID) public{
        AuctionTimeLimit = block.timestamp + AuctionDayLength_ days;
        highest_bid = startingBID;
    }

    function bid(uint256 amount) external payable returns(uint128){
        require(block.timestamp < AuctionTimeLimit);
        require(msg.value >= amount && amount > highest_bid);
        
        highest_bidder.transfer(highest_bid);
        highest_bid = amount;
        highest_bidder = msg.sender;
        



        event(msg.sender, amount)

    function 
        
        
    }  




}
