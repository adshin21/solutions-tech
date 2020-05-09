import unittest
import allocator


class TestSol(unittest.TestCase):

	def test_resource_allocator(self):
		result = allocator.resource_allocator('New York', 1150, 1)
		self.assertEqual("$10150", result['total_cost'])
		self.assertEqual([('8XLarge',7),('XLarge',1),('Large',1)], result['machines'])

		result = allocator.resource_allocator('India', 230, 1)
		self.assertEqual("$2133", result['total_cost'])
		self.assertEqual([('8XLarge',1),('2XLarge',1),('Large',3)], result['machines'])

		result = allocator.resource_allocator('China', 40, 1)
		self.assertEqual("$400", result['total_cost'])
		self.assertEqual([('XLarge',2)], result['machines'])



		result = allocator.resource_allocator('China', 1150, -1)
		self.assertEqual("Not a valid combination of time and units", result)
		
		result = allocator.resource_allocator('New York', -1150, 1)
		self.assertEqual("Not a valid combination of time and units", result)
		
		result = allocator.resource_allocator('New York', -1150, -1)
		self.assertEqual("Not a valid combination of time and units", result)

		result = allocator.resource_allocator('New York', 0, -1)
		self.assertEqual("Not a valid combination of time and units", result)


if __name__ == '__main__':
	unittest.main()
