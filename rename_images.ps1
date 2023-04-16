#
# Images are expected to be named by their hash.
# Therefore, will use Powershell to mass re-name
#

cd ".\images"

$i = 0;
foreach ($file in Get-ChildItem) {
    $md5Hash = Get-FileHash -Algorithm MD5 $file
    Write-Host "$($i): Renaming $($file.Name) to $($md5Hash.Hash)"
    Rename-Item $file.FullName -NewName $md5Hash.Hash
    $i++
}