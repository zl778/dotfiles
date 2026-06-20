- Sub MergeWorkbooks()
      Dim targetWorkbook As Workbook
      Dim sourceWorkbook As Workbook
      Dim ws As Worksheet
      
      Set targetWorkbook = ThisWorkbook
      
      '修改以下路径为源 Excel 文件的路径
      sourceFilePath = "C:\Path\To\Source\Workbook.xlsx"
      
      Set sourceWorkbook = Workbooks.Open(sourceFilePath)
      
      For Each ws In sourceWorkbook.Sheets
          ws.Copy After:=targetWorkbook.Sheets(targetWorkbook.Sheets.Count)
      Next ws
      
      sourceWorkbook.Close SaveChanges:=False '根据需要保存或不保存源文件
      
      End Sub
-