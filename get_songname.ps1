$itunesRunning = Get-Process iTunes -ErrorAction SilentlyContinue
if ($itunesRunning) {
	$itunes = New-Object -ComObject iTunes.Application
	$songInfo = $itunes.CurrentTrack
	$songInfo.Name
	$songInfo.Artist
}