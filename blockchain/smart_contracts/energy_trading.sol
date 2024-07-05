pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/token/ERC20/SafeERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/math/SafeMath.sol";

contract EnergyTrading {
    // Mapping of energy producers to their available energy
    mapping (address => uint256) public energyProducers;

    // Mapping of energy consumers to their energy demands
    mapping (address => uint256) public energyConsumers;

    // Mapping of energy trades to their details
    mapping (uint256 => Trade) public energyTrades;

    // Event emitted when a new energy trade is created
    event NewTrade(uint256 tradeId, address producer, address consumer, uint256 energyAmount);

    // Event emitted when an energy trade is fulfilled
    event TradeFulfilled(uint256 tradeId, address producer, address consumer, uint256 energyAmount);

    // Struct to represent an energy trade
    struct Trade {
        uint256 tradeId;
        address producer;
        address consumer;
        uint256 energyAmount;
        uint256 timestamp;
    }

    // Function to create a new energy trade
    function createTrade(address producer, address consumer, uint256 energyAmount) public {
        // Check if the producer has enough energy available
        require(energyProducers[producer] >= energyAmount, "Producer does not have enough energy available");

        // Check if the consumer has enough energy demand
        require(energyConsumers[consumer] >= energyAmount, "Consumer does not have enough energy demand");

        // Create a new trade
        uint256 tradeId = uint256(keccak256(abi.encodePacked(producer, consumer, energyAmount, block.timestamp)));
        energyTrades[tradeId] = Trade(tradeId, producer, consumer, energyAmount, block.timestamp);

        // Emit the NewTrade event
        emit NewTrade(tradeId, producer, consumer, energyAmount);
    }

    // Function to fulfill an energy trade
    function fulfillTrade(uint256 tradeId) public {
        // Get the trade details
        Trade storage trade = energyTrades[tradeId];

        // Check if the trade is valid
        require(trade.producer!= address(0) && trade.consumer!= address(0), "Invalid trade");

        // Transfer the energy from the producer to the consumer
        energyProducers[trade.producer] -= trade.energyAmount;
        energyConsumers[trade.consumer] -= trade.energyAmount;

        // Emit the TradeFulfilled event
        emit TradeFulfilled(tradeId, trade.producer, trade.consumer, trade.energyAmount);
    }

    // Function to add energy to a producer's available energy
    function addEnergy(address producer, uint256 energyAmount) public {
        energyProducers[producer] += energyAmount;
    }

    // Function to add energy demand to a consumer's energy demand
    function addDemand(address consumer, uint256 energyAmount) public {
        energyConsumers[consumer] += energyAmount;
    }
}
