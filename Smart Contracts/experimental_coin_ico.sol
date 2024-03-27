// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12 <0.9.0;

contract experimental_coin_ico {
    uint public max_experimental_coin = 1000000;
    uint public usd_to_experimental_coin = 1000;
    uint public total_experimental_coin_bought = 0;

    mapping(address => uint) equity_usd;
    mapping(address => uint) equity_experimental_coin;

    modifier can_buy_experimental_coin(uint usd_invested) {
        require(usd_invested * usd_to_experimental_coin + total_experimental_coin_bought <= max_experimental_coin);
        _;
    }

    function get_investor_equity_in_usd(address investor) external view returns(uint) {
        return equity_usd[investor];
    }

    function get_investor_equity_in_experimental_coin(address investor) external view returns(uint) {
        return equity_experimental_coin[investor];
    }
}