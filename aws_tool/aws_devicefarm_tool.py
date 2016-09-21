import os
import subprocess
import json
from time import sleep

aws = '/usr/local/aws/bin/aws'

# test data
project_arn = "arn:aws:devicefarm:us-west-2:825405415122:project:b50019bb-554c-4a9e-8e43-e06875aa5e00"
app_arn = "arn:aws:devicefarm:us-west-2:825405415122:upload:b50019bb-554c-4a9e-8e43-e06875aa5e00/f3797f10-f745-4f9b-9103-8ba90a4c7660"
app_type = "ANDROID_APP"
test_package_type = "APPIUM_PYTHON_TEST_PACKAGE"
test_run_type = "APPIUM_PYTHON"
test_package_arn = "arn:aws:devicefarm:us-west-2:825405415122:upload:b50019bb-554c-4a9e-8e43-e06875aa5e00/70dacb80-e31d-46f6-b9df-45b0117fefb2"
device_pool_arn = "arn:aws:devicefarm:us-west-2:825405415122:devicepool:b50019bb-554c-4a9e-8e43-e06875aa5e00/b987ae42-8894-4b40-bdaf-3ca9475dd355"

# process = subprocess.Popen([aws, 'devicefarm', 'list-projects'], stdout=subprocess.PIPE)
# out, err = process.communicate()


def exec_command(command):
    print "Command to execute= %s" % command
    output = None
    try:
        output = subprocess.check_output(command, shell=True)
        print "Command successfully executed."
    except:
        print "Failed to execute command."
    if output:
        print "Output= %s" % output
        return json.loads(output)
    return
# exec_command(aws + ' devicefarm list-projects')


def get_upload_status(arn):
    command = aws + " devicefarm get-upload --arn " + arn
    out = exec_command(command)
    upload_status = out['upload']['status']
    print "Upload status= %s" % upload_status
    return upload_status


def get_run_status(arn):
    command = aws + " devicefarm get-run --arn " + arn
    out = exec_command(command)
    run_status = out['run']['status']
    print "Test run status= %s" % run_status
    return run_status


def upload_file(upl_file, project_arn, upl_name, upl_type, check_interval=5):
    command1 = aws + ' devicefarm create-upload --project-arn ' + project_arn + ' --name ' + upl_name + ' --type ' + upl_type
    print "Executing command= %s" % command1
    out1 = exec_command(command1)
    if out1['upload']['status'] == "FAILED" or out1['upload']['type'] != upl_type:
        print "Failed to upload file!"
        return
    print "Upload link successfully created"

    upload_url = out1['upload']['url']
    upload_arn = out1['upload']['arn']

    command2 = "curl -T " + upl_file + " \"" + upload_url + "\""
    print "Executing command= %s" % command2
    out2 = exec_command(command2)

    i = 0
    while i < 3:
        if get_upload_status(upload_arn) == "SUCCEEDED":
            break
        sleep(check_interval)
        i += 1

    print "File successfully uploaded"

    return upload_arn


def upload_tests(test_file, project_arn, file_name='test_bundle.zip', test_type='APPIUM_PYTHON_TEST_PACKAGE'):
    return upload_file(upl_file=test_file, project_arn=project_arn, upl_name=file_name, upl_type=test_type)

# upload_tests(test_file="/Users/Andrii/development/AurumSoft/AWS/AWSTestEnvironment/test_bundle.zip", project_arn="arn:aws:devicefarm:us-west-2:825405415122:project:b50019bb-554c-4a9e-8e43-e06875aa5e00", file_name='test_bundle.zip', test_type='APPIUM_PYTHON_TEST_PACKAGE')


def upload_apk(apk_file, project_arn, app_name='test_app', app_type='ANDROID_APP'):
    return upload_file(upl_file=apk_file, project_arn=project_arn, upl_name=app_name, upl_type=app_type, check_interval=10)

# upload_apk("/Users/Andrii/development/AurumSoft/AWS/AWSTestEnvironment/application/Reader_release_arm7_12536_default_test.apk", project_arn="arn:aws:devicefarm:us-west-2:825405415122:project:b50019bb-554c-4a9e-8e43-e06875aa5e00", app_name='Reader_release_arm7_12536_default_test.apk', app_type='ANDROID_APP')


def schedule_test_run(project_arn, app_arn, device_pool_arn, run_name, test_type, test_package_arn, check_interval=60):

    test_json = "'{\"type\":\"" + test_type +"\",\"testPackageArn\":\"" + test_package_arn + "\"}'"
    print "Test json= %s" % test_json
    command = aws + " devicefarm schedule-run --project-arn " + project_arn + " --app-arn " + app_arn + " --device-pool-arn " + device_pool_arn + " --name \"" + run_name + "\" --test " + test_json
    print "Command= %s" % command
    out = exec_command(command)

    run_arn = out['run']['arn']

    i = 0
    while i < 30:
        if get_run_status(run_arn) == "COMPLETED":
            break
        sleep(check_interval)
        i += 1

    print "Test run completed."

    return run_arn


# print "Test run arn= %s" % schedule_test_run(project_arn=project_arn, app_arn=app_arn, device_pool_arn=device_pool_arn, run_name="Test Run 2", test_type=test_run_type, test_package_arn=test_package_arn)

#  TODO create device pool
#  TODO Full scenario