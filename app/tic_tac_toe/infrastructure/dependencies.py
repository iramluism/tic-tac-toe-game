from tic_tac_toe.domain import repositories as i_repositories
from tic_tac_toe.infrastructure import repositories

DEPENDENCIES = {
    i_repositories.IGameRepository: repositories.GameRepository,
    i_repositories.IPlayerRepository: repositories.PlayerRepository,
}
