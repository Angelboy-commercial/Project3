pragma solidity ^0.5.0;
// import "@openzeppelin/contracts-ethereum-package/contracts/math/SafeMath.sol";
import "./ArtRegistry.sol";

contract AuctionNFT{
    // using SafeMath for uint;
    
    uint256 AuctionTimeLimit;
    address payable public highest_bidder;
    uint256 highest_bid;
    address payable public beneficiary;
    uint256 highestBID;
    bool ended;
    string event_details;
    string NFTname;
    string NFTsymbol;
    mapping(address=>NFT) NFTowner;
    

    struct NFT{
        string NFTname;
        string NFTsymbol;
        string event_details;
    }

    event Bid(address bidder, uint256 amount);
    event AuctionOver(address winningBidder, uint256 amount);
    


    constructor(uint256 startingBID, uint256 AuctionTimeLimit_,address payable beneficiary_, string memory event_details_,
    string memory NFTname_, string memory NFTsymbol_) public{
        AuctionTimeLimit = block.timestamp + AuctionTimeLimit_;
        highestBID = startingBID;
        beneficiary = beneficiary_;
        event_details = event_details_;
        NFTname = NFTname_;
        NFTsymbol = NFTsymbol_;
        
        
        
    }

    function bid() public payable{
        require(block.timestamp < AuctionTimeLimit);
        require(msg.value > highest_bid);
        highest_bidder.transfer(highestBID);
        
        

        highestBID = msg.value;
        highest_bidder = msg.sender;

        

        emit Bid(msg.sender, msg.value);        
    }  
    
    


    function HighestBid() public view returns(uint256){
        return highestBID;
        

    }

    function Event_Details() public view returns (string memory){
        return event_details;
    }
    function AuctionEnd()public{
        require(ended == false);
        require(block.timestamp > AuctionTimeLimit);
        ended = true;
        beneficiary.transfer(highest_bid);
        emit AuctionOver(highest_bidder,highest_bid);


    }

    function CreateNFT() public returns (uint256){
        require(ended == true);
        require(highest_bidder == msg.sender);

        NFTowner[msg.sender] = NFT(NFTname, NFTsymbol,event_details);
        highest_bidder = address(beneficiary);
        

    }
    function viewToken() public view returns (string memory name){
        NFTowner[highest_bidder].NFTname;
        // NFTowner[highest_bidder].NFTsymbol;
        // NFTowner[highest_bidder].event_details;
        
    }




    
    // function TokenActive()public returns (string){
    //     NFTowner[msg.sender];
        
    // }
    // function BurnNFT()

     function() payable external{

     }



}
