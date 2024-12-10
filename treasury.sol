//SMART Contract for Treasury Management

//This contract collects fees, manages reserves, and integrates with an AI agent through an external call.



// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IAIRebalanceAgent {
    function suggestRebalance() external view returns (address[] memory, uint256[] memory);
}

contract JanusTreasury is Ownable {
    IERC20 public flatcoin; // JFT token
    IAIRebalanceAgent public aiAgent; // AI agent for portfolio management
    uint256 public totalReserves; // Total reserves in the treasury

    struct ReserveAsset {
        uint256 amount; // Amount of the asset held
        bool isActive; // Whether the asset is active in the treasury
    }

    mapping(address => ReserveAsset) public reserves;
    address[] public activeAssets;

    event RevenueCollected(address indexed from, uint256 amount);
    event AssetAllocated(address indexed asset, uint256 amount);
    event AssetWithdrawn(address indexed asset, uint256 amount);
    event Rebalanced(address[] assets, uint256[] amounts);

    constructor(address _flatcoin, address _aiAgent) {
        flatcoin = IERC20(_flatcoin);
        aiAgent = IAIRebalanceAgent(_aiAgent);
    }

    // Collect fees/revenue in flatcoins
    function collectRevenue(uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        flatcoin.transferFrom(msg.sender, address(this), amount);
        totalReserves += amount;

        emit RevenueCollected(msg.sender, amount);
    }

    // Allocate assets in the treasury
    function allocateAsset(address asset, uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than zero");
        ReserveAsset storage reserve = reserves[asset];

        if (!reserve.isActive) {
            reserve.isActive = true;
            activeAssets.push(asset);
        }

        reserve.amount += amount;
        emit AssetAllocated(asset, amount);
    }

    // Withdraw assets for rebalancing or other purposes
    function withdrawAsset(address asset, uint256 amount) external onlyOwner {
        ReserveAsset storage reserve = reserves[asset];
        require(reserve.amount >= amount, "Insufficient reserve balance");

        reserve.amount -= amount;
        IERC20(asset).transfer(owner(), amount);

        emit AssetWithdrawn(asset, amount);
    }

    // Rebalance portfolio based on AI agent's suggestions
    function rebalancePortfolio() external onlyOwner {
        // Get AI agent suggestions
        (address[] memory assets, uint256[] memory amounts) = aiAgent.suggestRebalance();

        require(assets.length == amounts.length, "Invalid AI agent response");

        // Apply rebalancing logic
        for (uint256 i = 0; i < assets.length; i++) {
            ReserveAsset storage reserve = reserves[assets[i]];

            if (!reserve.isActive) {
                reserve.isActive = true;
                activeAssets.push(assets[i]);
            }

            reserve.amount = amounts[i];
        }

        emit Rebalanced(assets, amounts);
    }

    // Get list of active assets
    function getActiveAssets() external view returns (address[] memory) {
        return activeAssets;
    }
}
