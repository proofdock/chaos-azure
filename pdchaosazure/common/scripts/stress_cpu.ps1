Param
(
    [parameter(mandatory=$true)] [int]$input_duration
)

"Input configuration: duration='$input_duration' seconds"

$number_of_parallel_procs=(Get-WMIObject win32_processor | Measure-Object NumberofLogicalProcessors -sum).sum
"Configuring number of parallel processes to '$max_number_of_cores'"

$code = {
    param ($duration)
    $stopwatch =  [system.diagnostics.stopwatch]::StartNew()
    $result = 1;
    while ($stopwatch.Elapsed.TotalSeconds -lt $duration) {
        $result = $result * $number
    }
}

"Stressing CPU with $number_of_parallel_procs processes for $input_duration seconds"
ForEach ($Number in 1..$number_of_parallel_procs){
    Start-Job -ScriptBlock $code -Arg $input_duration
}

Get-Job | Wait-Job