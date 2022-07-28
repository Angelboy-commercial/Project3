pragma solidity 0.6.0;
import "@openzeppelin/contracts-ethereum-package/contracts/math/SafeMath.sol";

contract Auction{
    using SafeMath for uint;
    
    uint256 AuctionTimeLimit;
    // address payable highest_bidder;
    // uint256 highest_bid;
    event Bid(address bidder, uint256 amount);
    uint256 highestBID;
    mapping(address => uint256) BidToOwner;

    constructor(uint256 startingBID) public{
        AuctionTimeLimit = block.timestamp + 3 days;
        highestBID = startingBID;
        uint8 AuctionDayLength_;
    }

    function bid(uint256 amount) public payable returns(uint128){
        require(block.timestamp < AuctionTimeLimit);
        require(msg.value >= amount && amount > highestBID);
        
        BidToOwner[amount] = msg.sender;
        BidToOwner[msg.sender] = msg.value;
        highestBID = amount;

        

        emit Bid(msg.sender, amount);        
    }  
    



    function CurrentBidder() public view returns (address){
        return BidToOwner[highestBID];
    }

    function HighestBid() public view returns(uint256){
        return highestBID;

    }

     fallback() payable external{

     }



}
