#r/工具/Excel

#excel宏 
Sub 公式转为值()
    ActiveCell.CurrentRegion.Copy 
    ActiveCell.CurrentRegion.PasteSpecial Paste:=xlPasteValues 
End Sub