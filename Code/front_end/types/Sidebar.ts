export interface SidebarItem {
  label: string;
  path: string;
}

export interface SidebarSection {
  title?: string;
  items: SidebarItem[];
}

export interface SidebarResponse {
  sections: SidebarSection[];
}