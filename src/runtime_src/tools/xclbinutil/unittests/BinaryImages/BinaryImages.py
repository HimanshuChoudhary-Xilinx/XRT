from argparse import RawDescriptionHelpFormatter
import argparse
import filecmp
import json
import os
import subprocess

# Start of our unit test
# -- main() -------------------------------------------------------------------
#
# The entry point to this script.
#
# Note: It is called at the end of this script so that the other functions
#       and classes have been defined and the syntax validated
def main():
  # -- Configure the argument parser
  parser = argparse.ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description='description:\n  Unit test wrapper for the various binary image sections')
  parser.add_argument('--resource-dir', nargs='?', default=".", help='directory containing data to be used by this unit test')
  args = parser.parse_args()

  # Validate that the resource directory is valid
  if not os.path.exists(args.resource_dir):
      raise Exception("Error: The resource-dir '" + args.resource_dir +"' does not exist")

  if not os.path.isdir(args.resource_dir):
      raise Exception("Error: The resource-dir '" + args.resource_dir +"' is not a directory")

  # Prepare for testing
  xclbinutil = "xclbinutil"

  # Start the tests
  print ("Starting test")

  # ---------------------------------------------------------------------------

  step = "1) Test Read / Writting of the Binary OVERLAY section"

  inputImage = os.path.join(args.resource_dir, "testimage.txt")
  outputImage = "overlay_image.txt"

  cmd = [xclbinutil, 
         "--add-section", "OVERLAY:RAW:" + inputImage, 
         "--dump-section", "OVERLAY:RAW:" + outputImage, 
         "--force"]
  execCmd(step, cmd)

  # Validate that the round trip files are identical
  binaryFileCompare(inputImage, outputImage)
  # ---------------------------------------------------------------------------

  step = "2) Test Read / Writting of the BITSTREAM section"

  inputImage = os.path.join(args.resource_dir, "testimage.txt")
  outputImage = "bitstream_image.txt"

  cmd = [xclbinutil, 
         "--add-section", "BITSTREAM:RAW:" + inputImage, 
         "--dump-section", "BITSTREAM:RAW:" + outputImage, 
         "--force"]
  execCmd(step, cmd)

  # Validate that the round trip files are identical
  binaryFileCompare(inputImage, outputImage)
  # ---------------------------------------------------------------------------

  step = "3) Test Read / Writting of the PDI section"

  inputImage = os.path.join(args.resource_dir, "testimage.txt")
  outputImage = "pdi_output.txt"

  cmd = [xclbinutil, 
         "--add-section", "PDI:RAW:" + inputImage, 
         "--dump-section", "PDI:RAW:" + outputImage, 
         "--force"]
  execCmd(step, cmd)

  # Validate that the round trip files are identical
  binaryFileCompare(inputImage, outputImage)
  # ---------------------------------------------------------------------------

  step = "4) Test Read / Writting of the USER_METADATA section"

  inputImage = os.path.join(args.resource_dir, "testimage.txt")
  outputImage = "user_output.txt"

  cmd = [xclbinutil, 
         "--add-section", "USER_METADATA:RAW:" + inputImage,
         "--dump-section", "USER_METADATA:RAW:" + outputImage, 
         "--force"]
  execCmd(step, cmd)

  # Validate that the round trip files are identical
  binaryFileCompare(inputImage, outputImage)
  # ---------------------------------------------------------------------------

  step = "5) Test Read / Writting of the AIE_RESOURCES section"

  inputImage = os.path.join(args.resource_dir, "testimage.txt")
  outputImage = "aie_resources_output.txt"

  cmd = [xclbinutil, 
         "--add-section", "AIE_RESOURCES:RAW:" + inputImage, 
         "--dump-section", "AIE_RESOURCES:RAW:" + outputImage, 
         "--force"]
  execCmd(step, cmd)

  # Validate that the round trip files are identical
  binaryFileCompare(inputImage, outputImage)
  # ---------------------------------------------------------------------------

  # If the code gets this far, all is good.
  return False

def binaryFileCompare(file1, file2):
    if not os.path.isfile(file1):
      raise Exception("Error: The following json file does not exist: '" + file1 +"'")

    if not os.path.isfile(file2):
      raise Exception("Error: The following json file does not exist: '" + file2 +"'")

    if filecmp.cmp(file1, file2) == False:
        print ("\nFile1 : "+ file1)
        print ("\nFile2 : "+ file2)

        raise Exception("Error: The two files are not binary the same")

def jsonFileCompare(file1, file2):
  if not os.path.isfile(file1):
    raise Exception("Error: The following json file does not exist: '" + file1 +"'")

  with open(file1) as f:
    data1 = json.dumps(json.load(f), indent=2)

  if not os.path.isfile(file2):
    raise Exception("Error: The following json file does not exist: '" + file2 +"'")

  with open(file2) as f:
    data2 = json.dumps(json.load(f), indent=2)

  if data1 != data2:
      # Print out the contents of file 1
      print ("\nFile1 : "+ file1)
      print ("vvvvv")
      print (data1)
      print ("^^^^^")

      # Print out the contents of file 1
      print ("\nFile2 : "+ file2)
      print ("vvvvv")
      print (data2)
      print ("^^^^^")

      raise Exception("Error: The two files are not the same")

def testDivider():
  print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def execCmd(pretty_name, cmd):
  testDivider()
  print(pretty_name)
  testDivider()
  cmdLine = ' '.join(cmd)
  print(cmdLine)
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  o, e = proc.communicate()
  print(o.decode('ascii'))
  print(e.decode('ascii'))
  errorCode = proc.returncode

  if errorCode != 0:
    raise Exception("Operation failed with the return code: " + str(errorCode))

# -- Start executing the script functions
if __name__ == '__main__':
  try:
    if main() == True:
      print ("\nError(s) occurred.")
      print("Test Status: FAILED")
      exit(1)
  except Exception as error:
    print(repr(error))
    print("Test Status: FAILED")
    exit(1)


# If the code get this far then no errors occured
print("Test Status: PASSED")
exit(0)

