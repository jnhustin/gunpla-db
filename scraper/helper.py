import os

class Helper():
  def make_dir(self, desired_location):
    if not os.path.exists(desired_location):
      os.mkdir(desired_location)
    return





if __name__ == '__main__':
  helper = Helper()
  locations = ['rg', 'mg', 'pg', 'sd', 'og']
  current_path     =  os.getcwd()
  dir_location     =  'html'

  for l in locations:
    desired_location =  f'{current_path}/{dir_location}/gundam_planet/{l}'
    helper.make_dir(desired_location)
