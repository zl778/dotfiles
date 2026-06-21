#r/工具/Excel

#r/工具/Excel 
- 使用宏：插入模块 excel多页合并一页
  Sub MergeSheets()
      Dim ws As Worksheet
      Dim combinedSheet As Worksheet
      
      Set combinedSheet = ThisWorkbook.Sheets.Add
      
      For Each ws In ThisWorkbook.Sheets
          If ws.Name <> combinedSheet.Name Then
              ws.UsedRange.Copy combinedSheet.Cells(combinedSheet.Cells(Rows.Count, 1).End(xlUp).Row + 1, 1)
          End If
      Next ws
  End Sub
-