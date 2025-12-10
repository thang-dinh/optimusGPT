// custom.d.ts
// Declare module for SVG files to allow importing them in TypeScript

declare module "*.svg" {
  const content: string;
  export default content;
}