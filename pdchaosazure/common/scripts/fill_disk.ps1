Param
(
    [parameter(mandatory=$true)] [int]$input_duration,
    [parameter(mandatory=$true)] [int]$input_size,
    [parameter(mandatory=$true)] [string]$input_path
)

$size_in_bytes = $input_size*1024*1024
"Input configuration: duration='$input_duration' seconds, size='$input_size' megabytes, path='$input_path'"

"Filling disk with $input_size megabytes of random data for $input_duration seconds."
# Check the https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-file
# Creates a file at $path of $size_in_bytes
fsutil file createnew $input_path $size_in_bytes
Start-Sleep -s $input_duration

"Cleaning up file at '$input_path' ..."
rm $input_path
"Cleaned up."