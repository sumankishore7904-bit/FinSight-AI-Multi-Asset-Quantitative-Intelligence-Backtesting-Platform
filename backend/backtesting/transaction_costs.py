def calculate_transaction_cost(
    portfolio_value: float,
    position_change: float,
    transaction_cost: float,
) -> float:
    """
    Transaction cost based on traded portfolio value.

    Example:
        100000 * 1.0 * 0.001 = 100
    """

    if portfolio_value < 0:
        raise ValueError(
            "Portfolio value cannot be negative."
        )

    if transaction_cost < 0:
        raise ValueError(
            "Transaction cost cannot be negative."
        )

    return abs(
        portfolio_value
        * position_change
        * transaction_cost
    )
