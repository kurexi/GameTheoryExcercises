from typing import List, Optional, Sequence, Tuple

from .strategic_form_game import TwoPlayerStrategicFormGame

StrategyMatrix = List[List[str]]
Payoff = Tuple[float, float]

STRATEGIES_ATTR = "_strategies"
PAYOFFS_ATTR = "_payoffs"
PRINTIBLE_ATTR = "printible"


def _clone_strategy_matrix(
    strategies: Optional[Sequence[Sequence[str]]]
) -> Optional[StrategyMatrix]:
    if strategies is None:
        return None
    cloned: StrategyMatrix = []
    for player_strategies in strategies:
        if isinstance(player_strategies, Sequence) and not isinstance(player_strategies, (str, bytes)):
            cloned.append(list(player_strategies))
        else:
            cloned.append([str(player_strategies)])
    return cloned


def _clone_payoff_matrix(
    payoffs: Optional[Sequence[Sequence[Payoff]]]
) -> Optional[List[List[Payoff]]]:
    if payoffs is None:
        return None
    return [list(row) for row in payoffs]


def _format_game(game: TwoPlayerStrategicFormGame, title: str = "TwoPlayerStrategicFormGame") -> str:
    lines = [title]
    lines.extend(_format_players_block(game))
    lines.extend(_format_payoff_block(game))
    return "\n".join(lines)


def _format_players_block(game: TwoPlayerStrategicFormGame) -> List[str]:
    block = []
    for idx in range(2):
        strategies = _get_player_strategies(game, idx)
        readable = ", ".join(strategies) if strategies else "—"
        block.append(f"  Player {idx + 1} strategies: {readable}")
    return block


def _format_payoff_block(game: TwoPlayerStrategicFormGame) -> List[str]:
    if not getattr(game, PAYOFFS_ATTR, None):
        return ["  Payoff matrix: <empty>"]

    player1_strats = _get_player_strategies(game, 0)
    player2_strats = _get_player_strategies(game, 1)

    if not player1_strats or not player2_strats:
        return [
            "  Payoff matrix: <incomplete — define strategies for both players to display>"
        ]

    table_lines = _render_payoff_table(game, player1_strats, player2_strats)
    indented = ["    " + line for line in table_lines]
    return ["  Payoff matrix (rows: Player 1, cols: Player 2):"] + indented


def _render_payoff_table(
    game: TwoPlayerStrategicFormGame, p1_strats: List[str], p2_strats: List[str]
) -> List[str]:
    table = _build_payoff_table(game, p1_strats, p2_strats)
    col_widths = [max(len(row[col]) for row in table) for col in range(len(table[0]))]

    rendered = []
    for idx, row in enumerate(table):
        padded = [row[col].ljust(col_widths[col]) for col in range(len(row))]
        rendered.append(" | ".join(padded))
        if idx == 0:
            separator = "-+-".join("-" * width for width in col_widths)
            rendered.append(separator)
    return rendered


def _build_payoff_table(
    game: TwoPlayerStrategicFormGame, p1_strats: List[str], p2_strats: List[str]
) -> List[List[str]]:
    header = ["P1 \\ P2"] + [str(strategy) for strategy in p2_strats]
    table = [header]
    for row_idx, p1_strategy in enumerate(p1_strats):
        row = [str(p1_strategy)]
        for col_idx in range(len(p2_strats)):
            row.append(_format_payoff_entry(game, row_idx, col_idx))
        table.append(row)
    return table


def _format_payoff_entry(game: TwoPlayerStrategicFormGame, row_index: int, column_index: int) -> str:
    payoffs = getattr(game, PAYOFFS_ATTR, []) or []
    if row_index >= len(payoffs):
        return "—"
    row = payoffs[row_index]
    if column_index >= len(row):
        return "—"
    entry = row[column_index]
    if isinstance(entry, tuple) and len(entry) == 2:
        return f"({entry[0]}, {entry[1]})"
    return str(entry)


def _get_player_strategies(game: TwoPlayerStrategicFormGame, player_index: int) -> List[str]:
    strategies = getattr(game, STRATEGIES_ATTR, []) or []
    if player_index >= len(strategies):
        return []
    player_strategies = strategies[player_index]
    return list(player_strategies) if isinstance(player_strategies, list) else [player_strategies]


class PrintableTwoPlayerStrategicFormGame(TwoPlayerStrategicFormGame):
    """Add-on subclass that provides readable string representations."""

    def __init__(
        self,
        strategies: Optional[StrategyMatrix] = None,
        payoffs: Optional[Sequence[Sequence[Payoff]]] = None,
    ) -> None:
        super().__init__(strategies=strategies, payoffs=payoffs)

    @classmethod
    def from_game(cls, game: TwoPlayerStrategicFormGame) -> "PrintableTwoPlayerStrategicFormGame":
        """Create a printable version from an existing game instance."""
        if isinstance(game, cls):
            return game
        strategies = _clone_strategy_matrix(getattr(game, STRATEGIES_ATTR, None))
        payoffs = _clone_payoff_matrix(getattr(game, PAYOFFS_ATTR, None))

        return cls(strategies=strategies, payoffs=payoffs)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(strategies={self.strategies!r}, "
            f"payoffs={self.payoffs!r})"
        )

    def __str__(self) -> str:
        return _format_game(self, title=self.__class__.__name__)


def _printible_property(game: TwoPlayerStrategicFormGame) -> str:
    return _format_game(game)


def _set_printible_attribute(cls: type, attribute_name: str = PRINTIBLE_ATTR) -> None:
    if not hasattr(cls, attribute_name):
        setattr(cls, attribute_name, property(_printible_property))


_set_printible_attribute(TwoPlayerStrategicFormGame)
