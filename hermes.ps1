



#set file paths. this should be pulled from options file but i've had some issues
$messageFile = "~/OneDrive/Apps/Commands/" + $args[0] + ".txt"
$history= "~/OneDrive/Apps/Commands/history"
$appDirectory = "~/OneDrive/Apps/Hermes"
$rulesFolder = "~/OneDrive/Apps/Hermes/rules"
#if a message exists process it
if (Test-Path -Path $messageFile -PathType leaf){
  #read the message
  $newMsg = Get-Content $messageFile | Out-String | ConvertFrom-Json


  #display the message
  write-host Device: $newMsg.device
  write-host Message: $newMsg.message
  write-host Timestamp: $newMsg.timestamp
  ## for each rule file
  Get-ChildItem $rulesFolder -Filter *.json | 
  Foreach-Object {
    ## read the patterns
    $rule = Get-Content $rulesFolder/$_ | Out-String | ConvertFrom-Json
    ## compare the message to each pattern
    foreach ($pattern in $rule.patterns){
      if ( $newMsg.message -match $pattern) {
        ## if the pattern is matched display the rule
        write-host ""
        write-host Rule: $rule.name
        write-host Pattern: $pattern
        write-host Active: $rule.active
        write-host ""
        if ($rule.active) {




          write-host Run Directory: $rule.runningDirectory
          write-host Run As Admin: $rule.runAsAdmin
          write-host Pass Message: $rule.passMessage
          write-host ""
          ## cd to the running directory
          cd $rule.runningDirectory
          ## Read the actions
          foreach ($action in $rule.actions) {
            ## execute the action
            if ( $rule.runAsAdmin -and $rule.passMessage ){
              write-host Action: $action $newMsg.message
              Start-Process -Verb RunAs cmd.exe -Args '/c', $action + " " + $newMsg.message
            } elseif ($rule.passMessage) {
              write-host Action: $action $newMsg.message
              Start-Process cmd.exe -Args '/c', $action $newMsg.message
            } elseif ($rule.runAsAdmin) {
              write-host Action: $action
              Start-Process -Verb RunAs cmd.exe -Args '/c', $action
            } else {
              write-host Action: $action
              Start-Process cmd.exe -Args '/c', $action
            }
          }
          break
        } else {
          write-host Rule is not active.
        }
      } 
    }		
  }
  ## cd back to the application directory
  cd $appDirectory
  ## backup the message
  md $history -ea 0
  Move-item $messageFile $history/$args.txt.$(get-date -f yyyyMMddHHmmss)
  ## ToDo: Add rule data / status to the history message
}
Start-Sleep -s 1
