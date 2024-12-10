// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IAIRebalanceAgent {
    function suggestRebalance() external view returns (address[] memory, uint256[] memory);
}
