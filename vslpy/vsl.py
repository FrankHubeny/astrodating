# vsl.py
"""The vsl class with its functions."""

from astropy import units as u
from astropy import constants as const

class vsl:
	"""Class for testing package setup with documentation and automation.  
	
	This version is not part of the plan for the actual package.  It only contains
	sample code to check the implication of pre-commits and continuous integration.
	"""
	
	def __init__(self, name: str):
		self.name = name
		
	def __str__(self):
        return self.name
		
	@u.quantity_input(speedfactor: u.dimensionless_unscaled)
	def lightspeed(speedfactor: float = 1):
		"""Returns the speed of light based on a variable speed factor.
		
		Parameters:
			speedfactor: The theoretically defined factor to obtain a speed of light.
				For constant speed of light theories this factor is 1, the default.
		
		Example:
			vsl.redshift()
			
		"""
		return speedfactor * const.C
		

					 