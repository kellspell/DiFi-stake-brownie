// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Kell_Token is ERC20 {
    constructor() public ERC20 ("KELL", "KT"){
        _mint(msg.sender, 1000000000000000000000000);

    }

}