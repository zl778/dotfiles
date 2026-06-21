#r/工具/Excel

#r/工具/Excel 
Sub 公式转为值()
    ActiveCell.CurrentRegion.Copy 
    ActiveCell.CurrentRegion.PasteSpecial Paste:=xlPasteValues 
End Sub