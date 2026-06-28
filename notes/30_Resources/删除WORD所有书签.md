#r/tools/Word

Sub 删除书签()
' 删除书签 宏
'
Dim MyBk As Bookmark
For Each MyBk In ActiveDocument.Bookmarks
MyBk.Delete
Next
End Sub