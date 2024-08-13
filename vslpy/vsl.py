# vsl.py
"""The vsl class with its functions."""

from astropy import constants as const


class VSL:
    """Class for testing package setup with documentation and automation.

    This version is not part of the plan for the actual package.  It
    only contains sample code to check the implication of pre-commits
    and continuous integration.
    """

    def __init__(self: "VSL", name: str) -> None:
        """Initialize the VSL clase."""
        self.name = name

    def __str__(self: "VSL") -> str:
        """Return the string value."""
        return self.name

    # @u.quantity_input(speedfactor: u.dimensionless_unscaled)
    def lightspeed(self: "VSL", speedfactor: float = 1) -> float:
        """Return the speed of light based on a variable speed factor.

        Args:
        ----
            speedfactor: The theoretically defined factor to obtain a speed of light.
                For constant speed of light theories this factor is 1, the default.

        Examples:
        --------
            >>> vsl.lightspeed()

        """
        return speedfactor * const.C
