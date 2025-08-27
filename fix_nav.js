const fs = require("fs");
const content = fs.readFileSync("frontend/src/pages/Block.jsx", "utf8");
const newContent = content.replace("const navigate = useNavigate()", `const navigate = useNavigate()

  const handleBackToBlocks = () => {
    const categoryId = blockCode.split("_")[0]
    navigate(\`/category/\${categoryId}\`)
  }`);
fs.writeFileSync("frontend/src/pages/Block.jsx", newContent);
console.log("Navigation function added successfully!");
