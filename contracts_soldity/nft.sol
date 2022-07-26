pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "./ArtRegistry.sol";

contract NFT is ERC721Full, ArtRegistry{

    mapping(uint => NFT) NFT_map;
    string NFTLink;
    mapping(address=>uint) CoinCirculation;
    string TwoTokenprize_;

    constructor(string memory NFT_name, string memory symbol,string memory NFTLink_) public ArtRegistry(NFT_name, symbol) {
        NFTLink = NFTLink_;
    }
   
    struct NFT{
        address BeneficiaryAddress;
        string EventDetails;
        
    }
   
    
    function PostNFT(address BeneficiaryAddress_, string memory EventDetails_)public returns(uint256){
        uint NFTid = totalSupply();
        


        return NFTid;

    }
    function TokensInCirculation()public view returns(uint){
        return CoinCirculation[msg.sender];
    }
    function TwoTokenprize(string memory details_)public {
        TwoTokenprize_ = details_;
        
        

    
        
    }

// function that checks if adress has two tokens therefore will be eligible for
// superprize that the celebrity has posted

}