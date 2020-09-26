Param
(
    [parameter(mandatory=$true)] [int]$input_duration,
    [parameter(mandatory=$true)] [string]$input_path
)

"Input configuration: duration='$input_duration' seconds, path='$input_path'"

New-Item -ItemType file $input_path

# Detect the block size of $input_path
$volume_label = Get-Volume -FilePath $input_path | Select-Object -ExpandProperty FileSystemLabel
"Volume label '$volume_label'"
$block_size = Get-CimInstance -ClassName Win32_Volume | Where-Object {$_.Label -eq "OS"} | Select-Object -ExpandProperty BlockSize
$file_size = $block_size*10000
"Detected block size='$block_size'"

$code = {
    # Expect those parameters from the calling job
    param ($input_path, $file_size)
    # Fill random data from cryptographic module with the length of $bytes in memory
    [System.Security.Cryptography.RNGCryptoServiceProvider] $rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
    $random_bytes = New-Object byte[] $file_size
    # Fill the array
    $rng.GetBytes($random_bytes)
    # Write the array content to file on disk. Do it continuously in a while loop and generate high I/O load
    while ($true) {
        [System.IO.File]::WriteAllBytes($input_path, $random_bytes)
    }
}


$job = Start-Job -ScriptBlock $code -ArgumentList $input_path,$file_size

# Clean job
if (Wait-Job $job -Timeout $input_duration) { Receive-Job $job }
Remove-Job -force $job

# Remove file
rm $input_path